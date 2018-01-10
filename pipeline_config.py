import os

from attrdict import AttrDict
from deepsense import neptune

from utils import read_yaml

ctx = neptune.Context()

try:
    params = ctx.params
    param_names = params.keys()
except AttributeError:
    neptune_config = read_yaml('config.yaml')
    params = neptune_config.parameters

X_COLUMNS = ['comment_text']
Y_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

SOLUTION_CONFIG = AttrDict({
    'env': {'cache_dirpath': params.experiment_dir},
    'fill_na': {'na_columns': X_COLUMNS},
    'xy_split': {'x_columns': X_COLUMNS,
                 'y_columns': Y_COLUMNS
                 },
    'char_tokenizer': {'char_level': True,
                       'maxlen': params.maxlen_char,
                       'num_words': params.max_features_char
                       },
    'word_tokenizer': {'char_level': False,
                       'maxlen': params.maxlen_words,
                       'num_words': params.max_features_word
                       },
    'tfidf_char_vectorizer': {'sublinear_tf': True,
                              'strip_accents': 'unicode',
                              'analyzer': 'char',
                              'token_pattern': r'\w{1,}',
                              'ngram_range': (1, params.char_ngram_max),
                              'max_features': params.max_features_char
                              },
    'tfidf_word_vectorizer': {'sublinear_tf': True,
                              'strip_accents': 'unicode',
                              'analyzer': 'word',
                              'token_pattern': r'\w{1,}',
                              'ngram_range': (1, 1),
                              'max_features': params.max_features_word
                              },
    'glove_embeddings': {'pretrained_filepath': params.embedding_filepath,
                         'max_features': params.max_features_word,
                         'embedding_size': params.word_embedding_size
                         },
    'glove_dpcnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(
                                                     params.trainable_embedding),
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_convo': params.l2_reg_convo,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_convo': params.dropout_convo,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'shuffle': True,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'glove_dpcnn_network',
                                     'glove_dpcnn_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'glove_scnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(
                                                     params.trainable_embedding),
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_convo': params.l2_reg_convo,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_convo': params.dropout_convo,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'shuffle': True,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'glove_scnn_network',
                                     'glove_scnn_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'glove_lstm_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(
                                                     params.trainable_embedding),
                                                 'unit_nr': params.filter_nr,
                                                 'repeat_block': params.repeat_block,
                                                 'global_pooling': bool(params.global_pooling),
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_lstm': params.dropout_lstm,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'glove_lstm_network',
                                     'glove_lstm_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'word_lstm_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'unit_nr': params.filter_nr,
                                                 'repeat_block': params.repeat_block,
                                                 'global_pooling': bool(params.global_pooling),
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_lstm': params.dropout_lstm,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints', 'word_lstm_network',
                                     'word_lstm_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'word_dpcnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(
                                                     params.trainable_embedding),
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_convo': params.l2_reg_convo,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_convo': params.dropout_convo,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'shuffle': True,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'word_dpcnn_network',
                                     'word_dpcnn_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'char_vdcnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_char,
                                                 'maxlen': params.maxlen_char,
                                                 'embedding_size': params.char_embedding_size,
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'l2_reg_convo': params.l2_reg_convo,
                                                 'l2_reg_dense': params.l2_reg_dense,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'dropout_convo': params.dropout_convo,
                                                 'dropout_dense': params.dropout_dense
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'char_vdcnn_network',
                                     'char_vdcnn_network.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {},
        },
    },
    'logistic_regression_multilabel': {'label_nr': 6,
                                       'C': params.log_reg_c,
                                       'solver': 'sag',
                                       'n_jobs': params.num_workers,
                                       },
    'logistic_regression_ensemble': {'label_nr': 6,
                                     'C': params.ensemble_log_reg_c,
                                     'n_jobs': params.num_workers,
                                     },
    'prediction_average': {'weights': params.weights
                           }
})
