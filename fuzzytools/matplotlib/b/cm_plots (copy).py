from __future__ import print_function
from __future__ import division
from . import _C

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from ..datascience.xerror import XError
from ..strings import xstr
from copy import copy, deepcopy
import matplotlib as mpl

DPI = _C.DPI
PLOT_FIGSIZE_CMAP = _C.PLOT_FIGSIZE_CMAP
CMAP = plt.cm.Reds

###################################################################################################################################################

def reorder_cms_classes(cms, classes, new_order_classes):
    assert len(cms.shape)==3 and cms.shape[1]==cms.shape[2] and cms.shape[1]==len(classes)

    plot_classes = new_order_classes.copy() if not new_order_classes is None else classes.copy()
    plot_classes = list(plot_classes)
    plot_classes_indexs = [plot_classes.index(c) for c in classes]

    cm_y = np.zeros_like(cms) # copy
    new_cms = np.zeros_like(cms) # copy
    for i,ind in enumerate(plot_classes_indexs):
        cm_y[:,ind,:] = cms[:,i,:]
    for i,ind in enumerate(plot_classes_indexs):
        new_cms[:,:,ind] = cm_y[:,:,i]

    return new_cms, plot_classes

###################################################################################################################################################

def plot_confusion_matrix(y_pred:np.ndarray, y_target:np.ndarray, class_names:list,
    new_order_classes:list=None,
    normalize_mode:str='true', # None, true, pred
    uses_percent:bool=True,
    english:bool=True,
    add_accuracy_in_title:bool=0,
    
    fig=None,
    ax=None,
    figsize=PLOT_FIGSIZE_CMAP,
    title='plot_custom_confusion_matrix',
    cmap=CMAP,
    fontsize=11,
    p=5,
    ):
    assert isinstance(class_names, list)
    assert y_pred.shape==y_target.shape
    assert y_pred.max()<=len(class_names)
    assert y_target.max()<=len(class_names)

    cms = confusion_matrix(y_target, y_pred)
    return plot_custom_confusion_matrix(cms, class_names,
        new_order_classes,
        normalize_mode,
        uses_percent,
        english,
        add_accuracy_in_title,
        
        fig,
        ax,
        figsize,
        title,
        cmap,
        fontsize,
        p,
        )

def plot_custom_confusion_matrix(cms:np.ndarray, class_names:list,
    new_order_classes:list=None,
    normalize_mode:str='true', # true, pred
    uses_percent:bool=True,
    english:bool=True,
    add_accuracy_in_title:bool=0,
    
    fig=None,
    ax=None,
    figsize=None,
    dpi=DPI,
    title='plot_custom_confusion_matrix',
    cmap=CMAP,
    fontsize=11,
    percentile=95,
    cbar_labelsize=7,
    ):
    '''
    Parameters
    ----------
    cms (b,c,c): b=batch of non-norm confusion matrixs
    '''
    ### checks
    assert isinstance(cms, np.ndarray) and 'int' in str(cms.dtype), 'must use non-norm confusion matrix for this function'
    assert isinstance(class_names, list)
    assert len(cms.shape)==3 and cms.shape[1]==cms.shape[2] and cms.shape[1]==len(class_names)

    ### processing
    cms, plot_classes = reorder_cms_classes(cms, class_names, new_order_classes)
    if normalize_mode=='true':
        cm_norm = cms.astype(np.float32)/(cms.sum(axis=2)[:,:,None])
    elif normalize_mode=='pred':
        cm_norm = cms.astype(np.float32)/(cms.sum(axis=1)[:,None,:])
    elif normalize_mode is None:
        cm_norm = cms.copy()
        uses_percent = False
    else:
        raise Exception(f'no mode {normalize_mode}')

    cms_xe = XError(cm_norm*100, 0)
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi) if fig is None else (fig, ax)
    ax.set(xticks=np.arange(len(plot_classes)), yticks=np.arange(len(plot_classes)))
    img = ax.imshow(cms_xe.median, interpolation='nearest', cmap=cmap)
    if uses_percent:
        boundaries = np.linspace(0, 100, 100//5+1)
        norm = mpl.colors.Normalize(vmin=0, vmax=100)
        cbar = ax.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        ticks = cbar.get_ticks()
        cbar.set_ticks(ticks)
        cbar.set_ticklabels([f'{t:.0f}%' for t in ticks])
        cbar.ax.tick_params(labelsize=cbar_labelsize)
    else:
        assert 0

    ax.set(xlabel='predicted label')
    ax.set(ylabel='true label')
    true_class_populations = np.sum(cms[0], axis=-1)
    balanced = all([tcp==true_class_populations[0] for tcp in true_class_populations])
    yticklabels = plot_classes if balanced else [f'{c}\n(${true_class_populations[kc]:,}$#)' for kc,c in enumerate(plot_classes)]
    ax.set(xticklabels=plot_classes, yticklabels=yticklabels)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')

    ### set titles
    if add_accuracy_in_title:
        acc_xe = XError(np.mean(np.diagonal(cm_norm, axis1=1, axis2=2), axis=-1)*100, 0)
        title += f'\n{"" if balanced else "b-"}accuracy={acc_xe}%'
    ax.set_title(title)
    
    ### add annotations
    thresh = cms_xe.median.max()/2.
    for i in range(len(plot_classes)):
        for j in range(len(plot_classes)):
            txt = f'{cms_xe.median[i,j]:.1f}'
            pi, pf = cms_xe.get_pbounds(percentile)
            superindex = xstr(pf[i,j]-cms_xe.median[i,j], add_pos=True)
            lowerindex = xstr(pi[i,j]-cms_xe.median[i,j], add_pos=True)
            txt = '${'+txt+'}^{'+superindex+'}_{'+lowerindex+'}$' if len(cms_xe)>1 else txt 
            ax.text(j, i, txt, ha='center', va='center',color='white' if cms_xe.median[i,j]>thresh else 'black', fontsize=fontsize)
            
    return fig, ax, cm_norm