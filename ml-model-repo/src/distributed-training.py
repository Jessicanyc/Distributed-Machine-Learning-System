import tensorflow_datasets as tfds
import tensorflow as tf
import json
import os
import argparse

from src.models import base_model, model_with_batchnorm, model_with_dropout

def make_datasets_unbatched():
    def scale(image, label):
        image = tf.cast(image, tf.float32)
        image /= 255
        return image, label
    datasets, _ = tfds.load(name='fashion_mnist', with_info=True, as_supervised=True)
    return datasets['train'].map(scale).cache().shuffle(10000)

def is_chief():
    tf_config = json.loads(os.environ.get('TF_CONFIG', '{}'))
    task_index = tf_config.get('task', {}).get('index', 0)
    return task_index == 0

def main(args):
    strategy = tf.distribute.MultiWorkerMirroredStrategy(
        communication_options=tf.distribute.experimental.CommunicationOptions(
            implementation=tf.distribute.experimental.CollectiveCommunication.AUTO))
    
    BATCH_SIZE_PER_REPLICA = 64
    BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

    with strategy.scope():
        ds_train = make_datasets_unbatched().batch(BATCH_SIZE).repeat()
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        ds_train = ds_train.with_options(options)
        
        if args.model_type == "cnn":
            multi_worker_model = base_model.build_and_compile_cnn_model()
        elif args.model_type == "dropout":
            multi_worker_model = model_with_dropout.build_and_compile_cnn_model_with_dropout()
        elif args.model_type == "batch_norm":
            multi_worker_model = model_with_batchnorm.build_and_compile_cnn_model_with_batch_norm()
        else:
            raise Exception("Unsupported model type: %s" % args.model_type)
        
        multi_worker_model.fit(ds_train, epochs=1, steps_per_epoch=70)
        
        model_path = args.saved_model_dir if is_chief() else args.saved_model_dir + '/worker_tmp_' + str(task_index)
        multi_worker_model.save(model_path)

if __name__ == "__main__":
    tfds.disable_progress_bar()

    parser = argparse.ArgumentParser()
    parser.add_argument('--saved_model_dir', type=str, required=True, help='Tensorflow export directory.')
    parser.add_argument('--checkpoint_dir', type=str, required=True, help='Tensorflow checkpoint directory.')
    parser.add_argument('--model_type', type=str, required=True, help='Type of model to train.')
    args = parser.parse_args()
    
    main(args)
