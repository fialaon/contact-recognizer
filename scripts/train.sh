#!/bin/bash


# ------------------------------------------------------------
# Configuration

#repo_dir=~/contact-recognizer
repo_dir=/app/contact-recognizer
exec_path=${repo_dir}/main.py
experiment_dir=${repo_dir}/train/results/acc_grandpa
#job_name=accuracy_neck
#job_name=accuracy_hands
#job_name=accuracy_knees
#job_name=accuracy_soles
job_name=accuracy_toes
#paths_training_data=${repo_dir}/data/joint_images/grandpa/neck_180.h5
#paths_training_data=${repo_dir}/data/joint_images/grandpa/hands_120.h5
#paths_training_data=${repo_dir}/data/joint_images/grandpa/knees_120.h5
#paths_training_data=${repo_dir}/data/joint_images/grandpa/soles_120.h5
paths_training_data=${repo_dir}/data/joint_images/grandpa/toes_120.h5
strides_training_data=1
models_folder=${repo_dir}/
#joint_name=neck
#joint_name=hands
#joint_name=knees
#joint_name=soles
joint_name=toes
num_trials=1
num_epochs=10
parameters_id=v1-lr-0.001
#resume=${repo_dir}/models/neck_180/checkpoints/v1-lr-0.005_7172a45d_neck_180.pth.tar
#resume=${repo_dir}/models/hands_120/checkpoints/v1-lr-0.001_df61e384_hands_120.pth.tar
#resume=${repo_dir}/models/knees_120/checkpoints/v1-lr-0.001_127696d5_knees_120.pth.tar
#resume=${repo_dir}/models/soles_120/checkpoints/v1-lr-0.0012_0ba883bc_soles_120.pth.tar
resume=${repo_dir}/models/toes_120/checkpoints/v1-lr-0.0012_db801a67_toes_120.pth.tar
# ------------------------------------------------------------
exec_settings="${experiment_dir} ${job_name} \
    ${paths_training_data} ${strides_training_data} \
    --models-folder=${models_folder} \
    --joint-name=${joint_name} \
    --num-trials=${num_trials} \
    --num-epochs=${num_epochs} \
    --parameters-id=${parameters_id}"

# if the $resume path is set to a non-empty string
if [ -n "${resume}" ]; then
    exec_settings="${exec_settings} --resume=${resume}"
fi

mkdir -p ${experiment_dir}

python3 ${exec_path} ${exec_settings}


#${repo_dir}/data/joint_images/handtool_train/hands_120.h5,${repo_dir}/data/joint_images/handtool_train_2/hands_120.h5,${repo_dir}/data/joint_images/parkour_train/hands_120.h5,