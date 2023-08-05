# -*- coding: utf-8 -*-

"""
Automated Tool for Optimized Modelling (ATOM)
Author: tvdboom
Description: Module containing plot functions.

"""


# << ============ Import Packages ============ >>

# Standard packages
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.model_selection import learning_curve
from sklearn.metrics import (
        SCORERS, roc_curve, precision_recall_curve, confusion_matrix
        )

# Own package modules
from .utils import check_is_fitted


# << ====================== Global variables ====================== >>

# List of tree-based models
tree_models = ['Tree', 'Bag', 'ET', 'RF', 'AdaB', 'GBM', 'XGB', 'LGB', 'CatB']


# << ======================== Plots ======================== >>

def plot_correlation(self, title, figsize, filename, display):

    """
    Correlation matrix plot of the dataset. Ignores non-numeric columns.

    PARAMETERS
    ----------
    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 10))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    # Compute the correlation matrix
    corr = self.dataset.corr()
    # Drop first row and last column (diagonal line)
    corr = corr.iloc[1:].drop(self.target, axis=1)

    # Generate a mask for the upper triangle
    # k=1 means keep outermost diagonal line
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask, k=1)] = True

    sns.set_style('white')  # Only for this plot
    fig, ax = plt.subplots(figsize=figsize)

    # Draw the heatmap with the mask and correct aspect ratio
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={'shrink': .5})

    title = "Feature correlation matrix" if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    fig.tight_layout()
    sns.set_style(self.style)  # Set back to original style
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_PCA(self, show, title, figsize, filename, display):

    """
    Plot the explained variance ratio of the components. Only if PCA
    was applied on the dataset through the feature_selection method.

    Parameters
    ----------
    show: int or None, optional (defalt=None)
        Number of components to show. If None, all are plotted.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=None)
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if not hasattr(self, 'PCA'):
        raise AttributeError("This plot is only availbale if you apply " +
                             "PCA on the dataset through the " +
                             "feature_selection method!")

    # Set parameters
    var = np.array(self.PCA.explained_variance_ratio_)
    if show is None or show > len(var):
        show = len(var)
    elif show < 1:
        raise ValueError("Invalid value for the show parameter." +
                         f"Value should be >0, got {show}.")
    if figsize is None:  # Default figsize depends on features shown
        figsize = (10, int(4 + show/2))

    scr = pd.Series(var, index=self.X.columns).nlargest(show).sort_values()

    fig, ax = plt.subplots(figsize=figsize)
    scr.plot.barh(label=f"Total variance retained: {round(var.sum(), 3)}",
                  width=0.6)
    for i, v in enumerate(scr):
        ax.text(v + 0.005, i - 0.08, f'{v:.3f}', fontsize=self.tick_fontsize)

    plt.title("Explained variance ratio", fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('Variance ratio', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Components', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    plt.xlim(0, max(scr) + 0.1 * max(scr))  # Make extra space for numbers
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_RFECV(self, title, figsize, filename, display):

    """
    Plot the scores obtained by the estimator fitted on every subset of
    the data. Only if RFECV was applied on the dataset through the
    feature_selection method.

    Parameters
    ----------
    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=None)
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if not hasattr(self, 'RFECV'):
        raise AttributeError("This plot is only availbale if you apply " +
                             "RFECV on the dataset through the " +
                             "feature_selection method!")

    try:  # Define the y-label for the plot
        ylabel = self.RFECV.get_params()['scoring'].name
    except AttributeError:
        if self.RFECV.get_params()['scoring'] is None:
            ylabel = 'score'
        else:
            ylabel = str(self.RFECV.get_params()['scoring'])

    fig, ax = plt.subplots(figsize=figsize)
    n_features = self.RFECV.get_params()['min_features_to_select']
    xline = range(n_features,  n_features + len(self.RFECV.grid_scores_))
    ax.axvline(xline[np.argmax(self.RFECV.grid_scores_)],
               ls='--',
               label=f'Best score: {round(max(self.RFECV.grid_scores_), 3)}')
    plt.plot(xline, self.RFECV.grid_scores_)

    plt.title("RFE cross-validation scores",
              fontsize=self.title_fontsize,
              pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('Number of features', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel(ylabel, fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    plt.xlim(n_features - 0.5, n_features + len(self.RFECV.grid_scores_) - 0.5)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Only int ticks
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_bagging(self, models, title, figsize, filename, display):

    """
    Plot a boxplot of the bagging's results.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    title: string or None, optional (default=None)
        Plot's title. If None, adapts size to the number of models.

    figsize: tuple, optional (default=None)
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    check_is_fitted(self._is_fitted)
    if not self.bagging:
        raise AttributeError("You need to run the pipeline using bagging" +
                             " before calling the plot_bagging method!")

    if models is None:
        models = [self.winner.name] if self.successive_halving else self.models
    elif isinstance(models, str):
        models = [models]

    results, names = [], []
    for model in models:
        if hasattr(self, model.lower()):
            results.append(getattr(self, model.lower()).bagging_scores)
            names.append(getattr(self, model.lower()).name)
        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    if figsize is None:  # Default figsize depends on number of models
        figsize = (int(8 + len(names)/2), 6)

    fig, ax = plt.subplots(figsize=figsize)
    plt.boxplot(results)

    title = 'Bagging results' if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.xlabel('Model', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel(self.metric.name,
               fontsize=self.label_fontsize,
               labelpad=12)
    ax.set_xticklabels(names)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_successive_halving(self, models, title, figsize, filename, display):

    """
    Plot of the models' scores per iteration of the successive halving.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 6))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    check_is_fitted(self._is_fitted)
    if not self.successive_halving:
        raise AttributeError("You need to run the pipeline using a " +
                             "successive halving approach before " +
                             "calling the plot_successive_halving method!")

    if models is None:
        models = self.scores[0].model  # List of models in first iteration
    elif isinstance(models, str):
        models = [models]

    # Define variables
    col = 'score_test' if self.bagging is None else 'bagging_mean'
    names = []
    liny = [[] for _ in models]
    filly = [[] for _ in models]

    for n, model in enumerate(models):
        if hasattr(self, model.lower()):  # If model in pipeline
            names.append(getattr(self, model.lower()).name)
            for m, df in enumerate(self.scores):
                if names[-1] in df.model.values:
                    idx = np.where(names[-1] == df.model.values)[0]
                    liny[n].append(df[col].iloc[idx].values[0])
                    if self.bagging is not None:
                        filly[n].append(df['bagging_std'].iloc[idx].values[0])
                else:
                    liny[n].append(np.NaN)
                    filly[n].append(np.NaN)
        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    fig, ax = plt.subplots(figsize=figsize)
    for y, std, label in zip(liny, filly, names):
        plt.plot(range(len(self.scores)), y, lw=2, marker='o', label=label)
        if self.bagging is not None:  # Fill the std area
            plt.fill_between(range(len(self.scores)),
                             [a + b for a, b in zip(y, std)],
                             [a - b for a, b in zip(y, std)],
                             alpha=0.4)
    plt.xlim(-0.1, len(self.scores)-0.9)

    title = "Successive halving results" if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('Iteration', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel(self.metric.name,
               fontsize=self.label_fontsize,
               labelpad=12)
    ax.set_xticks(range(len(self.scores)))
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_learning_curve(self, models, train_sizes, cv,
                        title, figsize, filename, display):

    """
    Plot the model's learning curve: score vs number of training samples. The
    `learning_curve` attribute is created, a dictionary of the plotted models
    containing the scores and fit duration per number of samples.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    train_sizes: sequence, optional (default=np.linspace(0.1, 1.0, 10))
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the dtype is float, it is regarded as a
        fraction of the maximum size of the training set. Otherwise it is
        interpreted as absolute sizes of the training sets.

    cv: int, sequence, callable or None, optional (default=None)
        Determines the cross-validation splitting strategy. Possible values:
            - None, to use the default 5-fold cross validation
            - int, to specify the number of folds in a (Stratified) KFold
            - CV splitter instance
            - An iterable yielding (train, test) splits as arrays of indices

        For int/None inputs, if the estimator is a classifier and y is
        either binary or multiclass, StratifiedKFold is used. In all other
        cases, KFold is used.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 6))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]

    self.learning_curve = {}
    fig, ax = plt.subplots(figsize=figsize)
    for model in models:
        if hasattr(self, model):
            m = getattr(self, model)

            # Get learning curve scores
            samples, train_scores, test_scores, time, _ = \
                learning_curve(m.best_model,
                               self.X_train,
                               self.y_train,
                               train_sizes=train_sizes,
                               cv=cv,
                               scoring=self.metric,
                               n_jobs=self.n_jobs,
                               return_times=True)

            train_scores_mean = np.mean(train_scores, axis=1)
            train_scores_std = np.std(train_scores, axis=1)
            test_scores_mean = np.mean(test_scores, axis=1)
            test_scores_std = np.std(test_scores, axis=1)
            time_mean = np.mean(time, axis=1)
            time_std = np.std(time, axis=1)

            # Draw line
            if len(models) == 1:
                label_train = f"Training score"
                label_test = f"Test score"
            else:
                label_train = f"{m.name} (Training score)"
                label_test = f"{m.name} (Test score)"
            plt.plot(samples, train_scores_mean, lw=2, label=label_train)
            plt.fill_between(samples,
                             train_scores_mean + train_scores_std,
                             train_scores_mean - train_scores_std,
                             alpha=0.4)
            plt.plot(samples, test_scores_mean, lw=2, label=label_test)
            plt.fill_between(samples,
                             test_scores_mean + test_scores_std,
                             test_scores_mean - test_scores_std,
                             alpha=0.4)

            # Append results to the attribute
            fraction = np.round(samples/len(self.X_train), 2)
            self.learning_curve[m.name] = \
                pd.DataFrame({'fraction of train_set': fraction,
                              'samples': samples,
                              'train_scores_mean': train_scores_mean,
                              'train_scores_std': train_scores_std,
                              'test_scores_mean': test_scores_mean,
                              'test_scores_std': test_scores_std,
                              'time_mean (s)': time_mean,
                              'time_std (s)': time_std})

        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    title = 'Learning curve' if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(fontsize=self.label_fontsize)
    plt.xlabel('Number of samples', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel(self.metric.name, fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_ROC(self, models, title, figsize, filename, display):

    """
    Plot the Receiver Operating Characteristics curve.
    Only for binary classification tasks.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10,6))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if not self.task.startswith('binary'):
        raise AttributeError("The plot_ROC method is only available for " +
                             "binary classification tasks!")

    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]

    fig, ax = plt.subplots(figsize=figsize)
    for model in models:
        if hasattr(self, model):
            m = getattr(self, model)

            # Get False (True) Positive Rate
            fpr, tpr, _ = roc_curve(m.y_test, m.predict_proba_test[:, 1])

            # Draw line
            if len(models) == 1:
                label = f"AUC={m.roc_auc:.3f}"
            else:
                label = f"{m.name} (AUC={m.roc_auc:.3f})"
            plt.plot(fpr, tpr, lw=2, label=label)

        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    plt.plot([0, 1], [0, 1], lw=2, color='black', linestyle='--')

    title = 'ROC curve' if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('FPR', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('TPR', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_PRC(self, models, title, figsize, filename, display):

    """
    Plot the precision-recall curve. Only for binary classification tasks.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 6))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if not self.task.startswith('binary'):
        raise AttributeError("The plot_PRC method is only available for " +
                             "binary classification tasks!")

    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]

    fig, ax = plt.subplots(figsize=figsize)
    for model in models:
        if hasattr(self, model):
            m = getattr(self, model)

            # Get precision-recall pairs for different probability thresholds
            predict_proba = m.predict_proba_test[:, 1]
            prec, recall, _ = precision_recall_curve(m.y_test, predict_proba)

            # Draw line
            if len(models) == 1:
                label = f"AP={m.average_precision:.3f}"
            else:
                label = f"{m.name} (AP={m.average_precision:.3f})"
            plt.plot(recall, prec, lw=2, label=label)

        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    title = "Precision-recall curve" if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower left', fontsize=self.label_fontsize)
    plt.xlabel('Recall', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Precision', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_permutation_importance(self, models, show, n_repeats,
                                title, figsize, filename, display):

    """
    Plot the feature permutation importance of models.

    PARAMETERS
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    show: int, optional (default=None)
        Number of best features to show in the plot. None for all.

    n_repeats: int, optional (default=10)
        Number of times to permute each feature.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional(default=(10, 6))
        Figure's size, format as (x, y).

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    # Set parameters
    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]
    if show is None:
        show = self.X.shape[1]
    elif show <= 0:
        raise ValueError("Invalid value for the show parameter." +
                         f"Value should be >0, got {show}.")
    if n_repeats <= 0:
        raise ValueError("Invalid value for the n_repeats parameter." +
                         f"Value should be >0, got {n_repeats}.")

    # Default figsize depends on features shown
    if figsize is None:
        figsize = (10, int(4 + show/2))

    # Create dataframe with columns as indices to plot with barh
    df = pd.DataFrame(columns=['features', 'score', 'model'])

    # Create dictionary to store the permutations per model
    self.permutations = {}

    for count, model in enumerate(models):
        if hasattr(self, model.lower()):
            m = getattr(self, model.lower())

            # Permutation importances returns Bunch object from sklearn
            # Force random state on function (won't work with numpy default)
            m.permutations = permutation_importance(
                                                m.best_model_fit,
                                                m.X_test,
                                                m.y_test,
                                                scoring=self.metric,
                                                n_repeats=n_repeats,
                                                n_jobs=self.n_jobs,
                                                random_state=self.random_state)

            # Assign attribute to ATOM class
            self.permutations[m.name] = m.permutations

            # Append data to the dataframe
            for i, feature in enumerate(self.X.columns):
                for score in m.permutations.importances[i, :]:
                    df = df.append({'features': feature,
                                    'score': score,
                                    'model': m.name},
                                   ignore_index=True)
        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    # Get the column names sorted by mean of score
    get_idx = df.groupby('features', as_index=False)['score'].mean()
    get_idx.sort_values('score', ascending=False, inplace=True)
    column_order = get_idx.features.values[:show]

    fig, ax = plt.subplots(figsize=figsize)
    sns.boxplot(x='score',
                y='features',
                hue='model',
                data=df,
                order=column_order,
                width=0.75 if len(models) > 1 else 0.6)

    title = 'Feature permutation importance' if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('Score', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Features', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_feature_importance(self, models, show,
                            title, figsize, filename, display):

    """
    Plot a tree-based model's normalized feature importance.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    show: int, optional (default=None)
        Number of best features to show in the plot. None for all.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=None)
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    # Set parameters
    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]
    if show is None:
        show = self.X.shape[1]
    elif show <= 0:
        raise ValueError("Invalid value for the show parameter." +
                         f"Value should be >0, got {show}.")

    # Create dataframe with columns as indices to plot with barh
    df = pd.DataFrame(index=self.X.columns)

    for model in models:
        if hasattr(self, model.lower()):
            m = getattr(self, model.lower())
            if m.name not in tree_models:
                raise AttributeError("The plot_feature_importance method is " +
                                     "only available for tree-based models, " +
                                     f"got {m.longname}!")

            # Bagging has no direct feature importance implementation
            if model == 'Bag':
                feature_importances = np.mean([
                    fi.feature_importances_ for fi in m.best_model.estimators_
                ], axis=0)
            else:
                feature_importances = m.best_model_fit.feature_importances_

            # Normalize for plotting values adjacent to bar
            df[m.name] = feature_importances/max(feature_importances)
        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    # Select best and sort ascending
    df = df.nlargest(show, columns=df.columns[-1])
    df.sort_values(by=df.columns[-1], ascending=True, inplace=True)

    if figsize is None:  # Default figsize depends on features shown
        figsize = (10, int(4 + show/2))

    # Plot figure
    width = 0.75 if len(models) > 1 else 0.6
    ax = df.plot.barh(figsize=figsize, width=width)
    if len(models) == 1:
        for i, v in enumerate(df[df.columns[0]]):
            ax.text(v + .01, i - .08, f'{v:.2f}', fontsize=self.tick_fontsize)

    title = "Normalized feature importance" if title is None else title
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(loc='lower right', fontsize=self.label_fontsize)
    plt.xlabel('Score', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Features', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    plt.xlim(0, 1.07)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_confusion_matrix(self, models, normalize,
                          title, figsize, filename, display):

    """
    For 1 model: plot it's confusion matrix in a heatmap.
    For >1 models: compare TP, FP, FN and TN in a barplot. Not supported for
                   multiclass classification.

    Parameters
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    normalize: bool, optional (default=False)
       Wether to normalize the matrix.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 10))
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if self.task == 'regression':
        raise AttributeError("The plot_confusion_matrix_method is only " +
                             "available for classification tasks!")

    # Set parameters
    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]

    if self.task.startswith('multiclass') and len(models) > 1:
        raise NotImplementedError("The plot_confusion_matrix method does not" +
                                  " support the comparison of various models" +
                                  " for multiclass classification tasks.")

    # Create dataframe to plot with barh if len(models) > 1
    df = pd.DataFrame(index=['True negatives',
                             'False positives',
                             'False negatives',
                             'True positives'])
    # Define title
    if title is None and normalize:
        title = "Normalized confusion matrix"
    elif title is None:
        title = "Confusion matrix"

    for model in models:
        if hasattr(self, model.lower()):
            # Compute confusion matrix
            cm = confusion_matrix(getattr(self, model.lower()).y_test,
                                  getattr(self, model.lower()).predict_test)

            if normalize:
                cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

            if len(models) == 1:  # Create matrix heatmap
                ticks = [v for v in self.mapping.keys()]

                fig, ax = plt.subplots(figsize=figsize)
                im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)

                # Create an axes on the right side of ax. The width of cax will
                # be 5% of ax and the padding between cax and ax will be fixed
                # at 0.3 inch.
                divider = make_axes_locatable(ax)
                cax = divider.append_axes("right", size="5%", pad=0.3)
                cbar = ax.figure.colorbar(im, cax=cax)
                ax.set(xticks=np.arange(cm.shape[1]),
                       yticks=np.arange(cm.shape[0]),
                       xticklabels=ticks,
                       yticklabels=ticks)

                # Loop over data dimensions and create text annotations
                fmt = '.2f' if normalize else 'd'
                for i in range(cm.shape[0]):
                    for j in range(cm.shape[1]):
                        ax.text(j, i, format(cm[i, j], fmt),
                                ha='center', va='center',
                                fontsize=self.tick_fontsize,
                                color='w' if cm[i, j] > cm.max() / 2. else 'k')

                ax.set_title(title, fontsize=self.title_fontsize, pad=12)
                ax.set_xlabel('Predicted label',
                              fontsize=self.label_fontsize,
                              labelpad=12)
                ax.set_ylabel('True label',
                              fontsize=self.label_fontsize,
                              labelpad=12)
                cbar.set_label('Counts',
                               fontsize=self.label_fontsize,
                               labelpad=15,
                               rotation=270)
                cbar.ax.tick_params(labelsize=self.tick_fontsize)
                ax.grid(False)

            else:  # Create barplot
                df[getattr(self, model.lower()).name] = cm.ravel()

        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    if len(models) > 1:
        df.plot.barh(figsize=figsize, width=0.6)
        plt.xlabel('Counts', fontsize=self.label_fontsize, labelpad=12)
        plt.title(title, fontsize=self.title_fontsize, pad=12)
        plt.legend(fontsize=self.label_fontsize)

    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_threshold(self, models, metric, steps,
                   title, figsize, filename, display):

    """
    Plot performance metric(s) against multiple threshold values.

    PARAMETERS
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    metric: string, callable, list, tuple or None, optional (default=None)
        Metric(s) to plot. These can be one of the pre-defined sklearn scorers
        as string, a metric function or a sklearn scorer object. If None, the
        metric used to fit the pipeline is used.

    steps: int, optional (default=100)
        Number of thresholds measured.

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 10))
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if not self.task.startswith('binary'):
        raise AttributeError("The plot_threshold method is only available " +
                             "for binary classification tasks!")

    # Set parameters
    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]
    if metric is None:
        metric = [self.metric]
    elif not isinstance(metric, list):
        metric = [metric]

    # Convert all strings to functions
    metric_list = []
    for met in metric:
        if isinstance(met, str):  # It is one of sklearn predefined metrics
            if met not in SCORERS.keys():
                raise ValueError("Unknown value for the metric parameter, " +
                                 f"got {met}. Try one of {SCORERS.keys()}.")
            metric_list.append(getattr(self.metric, met)._score_func)
        elif hasattr(met, '_score_func'):  # It is a scorer
            metric_list.append(met._score_func)
        else:  # It is a metric function
            metric_list.append(met)

    fig, ax = plt.subplots(figsize=figsize)
    steps = np.linspace(0, 1, steps)
    for model in models:
        if hasattr(self, model.lower()):
            m = getattr(self, model.lower())

            for met in metric_list:  # Create dict of empty arrays
                results = []
                for step in steps:
                    pred = (m.predict_proba_test[:, 1] >= step).astype(bool)
                    results.append(met(m.y_test, pred))

                # Draw the line for each metric
                if len(models) == 1:
                    label = met.__name__
                else:
                    label = f"{m.name} ({met.__name__})"
                plt.plot(steps, results, label=label, lw=2)

        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    if title is None:
        temp = '' if len(metric) == 1 else 's'
        title = f"Performance metric{temp} against threshold value"
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(fontsize=self.label_fontsize)
    plt.xlabel('Threshold', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Score', fontsize=self.label_fontsize, labelpad=12)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


def plot_probabilities(self, models, target,
                       title, figsize, filename, display):

    """
    Plot a function of the probability of the classes
    of being the target class.

    PARAMETERS
    ----------
    models: string, list, tuple or None, optional (default=None)
        Name of the models to plot. If None, all the models in the
        pipeline are selected.

    target: int or string, optional (default=1)
        Probability of being that class (as index or name).

    title: string or None, optional (default=None)
        Plot's title. If None, the default option is used.

    figsize: tuple, optional (default=(10, 10))
        Figure's size, format as (x, y). If None, adapts size to `show` param.

    filename: string or None, optional (default=None)
        Name of the file (to save). If None, the figure is not saved.

    display: bool, optional (default=True)
        Wether to render the plot.

    """

    if self.task == 'regression':
        raise AttributeError("The plot_probabilities method is only " +
                             "available for classification tasks!")

    # Set parameters
    check_is_fitted(self._is_fitted)
    if models is None:
        models = self.models
    elif isinstance(models, str):
        models = [models]

    # Make target mapping
    inv_map = {str(int(v)): k for k, v in self.mapping.items()}
    if isinstance(target, str):  # User provides a string
        target_int = self.mapping[target]
        target_str = target
    else:  # User provides an integer
        target_int = target
        target_str = inv_map[str(target)]

    fig, ax = plt.subplots(figsize=figsize)
    for model in models:
        if hasattr(self, model.lower()):
            m = getattr(self, model.lower())
            if not hasattr(m, 'predict_proba_test'):
                raise ValueError("The plot_probabilities method is only " +
                                 "available for models with a " +
                                 "predict_proba method!")

            for key, value in self.mapping.items():
                idx = np.where(m.y_test == value)[0]  # Get indices per class
                if len(models) == 1:
                    label = f"Class={key}"
                else:
                    label = f"{m.name} (Class={key})"
                sns.distplot(m.predict_proba_test[idx, target_int],
                             hist=False,
                             kde=True,
                             norm_hist=True,
                             kde_kws={'shade': True},
                             label=label)
        else:
            raise ValueError(f"Model {model} not found in pipeline!")

    if title is None:
        title = f"Predicted probabilities for {m.y_train.name}={target_str}"
    plt.title(title, fontsize=self.title_fontsize, pad=12)
    plt.legend(fontsize=self.label_fontsize)
    plt.xlabel('Probability', fontsize=self.label_fontsize, labelpad=12)
    plt.ylabel('Counts', fontsize=self.label_fontsize, labelpad=12)
    plt.xlim(0, 1)
    plt.xticks(fontsize=self.tick_fontsize)
    plt.yticks(fontsize=self.tick_fontsize)
    fig.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show() if display else plt.close()


# << ====================== Utilities ====================== >>

def save(self, filename):

    """
    Save class to a pickle file.

    Parameters
    ----------
    filename: str or None, optional (default=None)
        Name of the file when saved (as .html). None to not save anything.

    """

    filename = filename if filename.endswith('.pkl') else filename + '.pkl'
    pickle.dump(self, open(filename, 'wb'))
