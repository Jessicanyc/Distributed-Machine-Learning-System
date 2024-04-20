import json
import os
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.metrics import SparseCategoricalAccuracy
from transformers import BertTokenizer, TFBertModel, BertConfig

# Configuration for a hypothetical cluster. 
#tells each instance of the application which part of the distributed setup it is (which worker it is) and how to communicate with the other parts of the syste
# no need when using tfjob.yaml
# os.environ['TF_CONFIG'] = json.dumps({
#     'cluster': {
#         'worker': ["host1:port", "host2:port", "host3:port"]
#     },
#     'task': {'type': 'worker', 'index': 0}
# })

strategy = tf.distribute.MultiWorkerMirroredStrategy()

with strategy.scope():
    # Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    bert_config = BertConfig.from_pretrained('bert-base-uncased', output_hidden_states=True)
    model = TFBertModel.from_pretrained('bert-base-uncased', config=bert_config)

    # Example simple model setup
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss=SparseCategoricalCrossentropy(from_logits=True),
        metrics=[SparseCategoricalAccuracy()]
    )

def encode_examples(texts, max_length):
    # Tokenize the texts
    return dict(tokenizer(texts, padding="max_length", truncation=True, max_length=max_length, return_tensors="tf"))

# Example texts and labels
texts = ["Hello world", "TensorFlow with Kubernetes"]
labels = [1, 0]  # Example labels for classification

# Convert to TensorFlow dataset
train_dataset = tf.data.Dataset.from_tensor_slices((texts, labels))
train_dataset = train_dataset.map(lambda x, y: (encode_examples(x, max_length=128), y))
train_dataset = train_dataset.batch(2)  # Batch size can be adjusted

# Execute training
model.fit(train_dataset, epochs=3, steps_per_epoch=10)  # Adjust epochs and steps per epoch as needed
