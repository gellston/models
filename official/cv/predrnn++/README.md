# Contents

- [Contents](#contents)
    - [Predrnn++ Description](#predrnn-description)
    - [Model Architecture](#model-architecture)
    - [Dataset](#dataset)
        - [Dataset Prepare](#dataset-prepare)
    - [Environment Requirements](#environment-requirements)
    - [Quick Start](#quick-start)
    - [Script Description](#script-description)
        - [Script and Sample Code](#script-and-sample-code)
        - [Script Parameters](#script-parameters)
            - [Training Script Parameters](#training-script-parameters)
    - [Training Process](#training-process)
        - [Training](#training)
    - [Evaluation Process](#evaluation-process)
        - [Evaluation](#evaluation)
    - [Model Description](#model-description)
        - [Performance](#performance)
            - [Training Performance](#training-performance)
            - [Evaluation Performance](#evaluation-performance)
    - [ModelZoo Homepage](#modelzoo-homepage)

## [Predrnn++ Description](#contents)

PredRNN++ is an improved recurrent network for video predictive learning. In pursuit of a greater spatiotemporal modeling capability, our approach increases the transition depth between adjacent states by leveraging a novel recurrent unit, which is named Causal LSTM for re-organizing the spatial and temporal memories in a cascaded mechanism. However, there is still a dilemma in video predictive learning: increasingly deep-in-time models have been designed for capturing complex variations, while introducing more difficulties in the gradient back-propagation. To alleviate this undesirable effect, we propose a Gradient Highway architecture, which provides alternative shorter routes for gradient flows from outputs back to long-range inputs. This architecture works seamlessly with causal LSTMs, enabling PredRNN++ to capture short-term and long-term dependencies adaptively. We assess our model on both synthetic and real video datasets, showing its ability to ease the vanishing gradient problem and yield state-of-the-art prediction results even in a difficult objects occlusion scenario.

[Paper](https://arxiv.org/pdf/1804.06300v2.pdf): Yunbo Wang, Zhifeng Gao, Mingsheng Long, Jian-Min Wang, Philip S. Yu, "PredRNN++: Towards A Resolution of the Deep-in-Time Dilemma in Spatiotemporal Predictive Learning", arXiv:1804.06300v2 [cs.LG] 19 Nov 2018

## [Model Architecture](#content)

Predrnn+ has a 5-layer architecture, in pursuit of high prediction quality with reasonable training time and memory usage, consisting of 4 causal LSTMs with 128, 64, 64, 64 channels respectively, as well as a 128-channel gradient highway unit on the top of the bottom causal LSTM layer. We also set the
convolution filter size to 5 inside all recurrent units.

Compared with the above deep-in-time recurrent architectures, our approach has two key insights: First, it presents a new spatiotemporal memory mechanism, causal LSTM, in order to increase the recurrence depth from one time step to the next, and by this means, derives a more powerful modeling capability to stronger spatial correlations and short-term dynamics. Second, it attempts to solve gradient back-propagation issues for the sake of long-term video modeling. It constructs an alternative gradient highway, a shorter route from future outputs back to distant inputs.

## [Dataset](#content)

Note that you can run the scripts based on the dataset mentioned in original paper or widely used in relevant domain/network architecture. In the following sections, we will introduce how to run the scripts using the related dataset below.

We use the moving mnist dataset (http://www.cs.toronto.edu/~nitish/unsupervised_video/) mentioned in the paper for training and evaluation.

### [Dataset Prepare](#content)

The moving mnist dataset from the official website contains 3 files: train/valid/test.npz. Use generate_mindrecord.py to convert dataset to mindrecord format, DATASET_PATH is the path of the moving mnist dataset folder:

```shell
    $ python generate_mindrecord.py --dataset_path=[DATASET_PATH]
```

## [Environment Requirements](#contents)

- Hardware
    - Prepare hardware environment with Ascend.
- Framework
    - [MindSpore](https://gitee.com/mindspore/mindspore)
- For more information, please check the resources below：
    - [MindSpore Tutorials](https://www.mindspore.cn/tutorials/en/master/index.html)
    - [MindSpore Python API](https://www.mindspore.cn/docs/api/en/master/index.html)

## [Quick Start](#contents)

- After the dataset is prepared, you may start running the training script as follows:

    - Running on Ascend

    ```bash
    # standalone training example in Ascend
    # TRAIN_MINDRECORD_PATH is the path of the file mnist_train.mindrecord
    $ bash scripts/run_standalone_train.sh [TRAIN_MINDRECORD_PATH] [DEVICE_ID]
    ```

## [Script Description](#contents)

### [Script and Sample Code](#contents)

```shell
Predrnn++
├── README.md
├── generate_mindrecord.py                      # Convert moving mnist dataset to mindrecord
├── requirements.txt
├── scripts
│   ├── run_eval.sh                             # Launch evaluation in Ascend
│   └── run_standalone_train.sh                 # Launch standalone training in Ascend (1 pcs)
├── nets
│   ├── predrnn_pp.py                           # Model definition
├── layers
│   ├── LayerNorm.py
│   ├── GradientHighwayUnit.py
│   ├── CausalLSTMCell.py
│   ├── BLoss.py                                # Loss function
├── data_provider
│   ├── mnist_to_mindrecord.py                  # Dataset conversion
│   ├── mnist.py                                # Moving mnist dataset preprocess
│   ├── datasets_factory.py
│   ├── preprocess.py                           # Default configurations
├── metrics.py                                  # Evaluation metric functions
├── config.py                                   # Dataset patch functions
├── train.py                                    # Training script
├── eval.py                                     # Evaluation script
├── default_config.yaml                         # Config file
```

### [Script Parameters](#contents)

#### Training Script Parameters

```shell

#### Parameters Configuration

Parameters for both training and evaluation can be set in default_config.yaml.

```

train_mindrecord: ""                            # path to train dataset
test_mindrecord: ""                             # path to test dataset
pretrained_model: ""                            # path to pretrained model
save_dir: "./"                                  # path to save model checkpoint
model_name: "predrnn_pp"                        # model name
input_length: 10                                # length of input sequence
seq_length: 20                                  # length of total sequence
img_width: 64                                   # width of input image
img_channel: 1                                  # number of input image channels
stride: 1                                       # stride of convlstm layer
filter_size: 5                                  # filter size of convlstm layer
num_hidden: '128,64,64,64'                      # number of units in a convlstm layer
patch_size: 4                                   # input patch size in one dimension
layer_norm: True                                # whether to apply tensor layer norm
lr: 0.001                                       # base learning rate
reverse_input: True                             # whether to reverse the input frames while training
batch_size: 8                                   # batch size for training
max_iterations: 80000                           # total number of training steps
snapshot_interval: 1000                         # number of iters to save models
sink_size: 10                                   # number of data to sink per epoch
device_num: 1                                   # number of NPU used
device_id: 0                                    # id of NPU used

```lang-yaml

## [Training Process](#contents)

- Set options in `config.py`, including learning rate and other network hyperparameters. Click [MindSpore dataset preparation tutorial](https://www.mindspore.cn/tutorials/en/master/advanced/dataset.html) for more information about dataset.

### [Training](#contents)

- Run `run_standalone_train.sh` for non-distributed training of Predrnn++ model on Ascend.

``` bash

bash scripts/run_standalone_train.sh [TRAIN_MINDRECORD_PATH] [DEVICE_ID]

```

## [Evaluation Process](#contents)

### [Evaluation](#contents)

- Run `run_eval.sh` for evaluation. TEST_MINDRECORD_PATH is the path of the file mnist_test.mindrecord

``` bash

bash scripts/run_eval.sh [TEST_MINDRECORD_PATH] [DEVICE_ID] [CHECKPOINT_PATH]

```

Check the `eval/log.txt` and you will get outputs as following:

```shell

mse per frame: 47.858854093653633
    20.98119093135079
    27.252088156613436
    33.403171304712956
    39.82251721652434
    45.859534120814686
    51.62611664042753
    57.17143022567831
    62.79542451746323
    67.35081808324804
    72.32624973970302

```

## [Model Description](#contents)

### [Performance](#contents)

#### [Training Performance](#contents)

| Parameters                 | Ascend 910                                        |
| -------------------------- | --------------------------------------------------|
| Resource                   | Ascend 910; CPU 2.60GHz, 192cores; Memory 755G; OS Euler2.8
| uploaded Date              | 1/15/2022 (month/day/year)                        |
| MindSpore Version          | 1.6.0                                             |
| Dataset                    | moving mnist                                      |
| Training Parameters        | epoch=8000, steps per epoch=10, batch_size=8      |
| Optimizer                  | Adam                                              |
| Loss Function              | L2Loss                                            |
| Loss                       | 165.70367431640625                                |
| Speed                      | 1000 ms/step(1pcs)                                |
| Total time                 | 22h                                               |
| Checkpoint for Fine tuning | 177.27M (.ckpt file)                              |
| Scripts                    | [Link](https://gitee.com/mindspore/models/tree/master/official/cv/predrnn++) |

#### [Evaluation Performance](#contents)

| Parameters          |                             |
| ------------------- | --------------------------- |
| Resource            | Ascend 910; OS Euler2.8     |
| Uploaded Date       | 1/15/2022 (month/day/year)  |
| MindSpore Version   | 1.6.0                       |
| Dataset             | moving mnist                |
| batch_size          | 8                           |
| output metrics      | MSE/SSIM                    |
| outputs             | 47.9/0.878                  |
| Model for inference | 177.27M (.ckpt file)        |

## [ModelZoo Homepage](#contents)

Please check the official [homepage](https://gitee.com/mindspore/models)