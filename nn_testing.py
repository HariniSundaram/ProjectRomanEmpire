# -*- coding: utf-8 -*-
"""NN_Testing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-L0YQt1RkLUA-8LqczF3u-WfbXAsixTj
"""

!pip install torchvision

import torch
from torchsummary import summary
import torchvision #This library is used for image-based operations (Augmentations)
import os
import gc
from tqdm import tqdm
from PIL import Image
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import glob
import matplotlib.pyplot as plt
# from torchinfo import summary # (or this if torchsummary sucks (sometimes breaks in current version))
import torch.nn.functional as F
import torch.nn as nn
from google.colab import drive

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print("Device: ", device)

config = {
    'batch_size': 256,
    'lr': 0.1,
    'epochs': 25,
    'weight_decay' : 0.00001,
    'dropout' : 0.3
}

from google.colab import drive
drive.mount('/content/drive')

df_train = pd.read_csv("/content/large_train.csv")
df_test = pd.read_csv("/content/large_test.csv")
df_val = pd.read_csv("/content/large_val.csv")


def safe_convert_to_float(value):
    if pd.isna(value):
        # Directly return pandas.NA if the value is NA or NaN
        return pd.NA
    try:
        # Attempt to convert the value to float
        return np.float64(value)
    except ValueError:
        # Return None or np.nan if the conversion fails
        return pd.NA

import pandas as pd

def process_dataframe(df):
    features = ['daily_rain_sum', 'daily_temperature_2m_max', 'daily_temperature_2m_min', "daily_temperature_2m_max", 'daily_precipitation_sum', 'daily_rain_sum', 'daily_snowfall_sum', 'daily_wind_speed_10m_max', 'daily_wind_gusts_10m_max']

    # Ensure all values are numeric (floats)
    for feature in features:
        # Convert any non-numeric values to NaN, then to float
        df[feature] = pd.to_numeric(df[feature].apply(lambda x: x.strip("[]") if isinstance(x, str) else x), errors='coerce')

    return df

df_train.to_csv("clean_train.csv", sep='\t', index="False")
df_val.to_csv("clean_val.csv", sep='\t', index="False")
df_test.to_csv("clean_test.csv", sep='\t', index="False")

process_dataframe(df_train)
process_dataframe(df_test)
process_dataframe(df_val)

threshold = 100  # Example threshold, adjust based on your understanding of the data
normalized_training = df_train[(df_train['risk_factor'] <= threshold) & (df_train['risk_factor'] >= 0)]
normalized_test = df_test[(df_test['risk_factor'] <= threshold) & (df_test['risk_factor'] >= 0)]
normalized_val = df_val[(df_val['risk_factor'] <= threshold) & (df_val['risk_factor'] >= 0)]

normalized_test = normalized_test.iloc[:, 1:]
normalized_val = normalized_val.iloc[:, 1:]

class PLSDataset(torch.utils.data.Dataset):
    def __init__(self, df):
        # Read the CSV file into a DataFrame
        columns_to_drop = ["start city name", "intermediate city name", "date", "start city coordinates", "intermediate city coordinates"]

        # Drop the specified columns
        df = df.drop(columns=columns_to_drop)

        # Separate features and labels
        self.labels = np.array(df['risk_factor'])

        #df = df.drop("risk_factor")

        self.features = df.to_numpy()

        assert len(self.features) == len(self.labels), "Features and labels must have the same length"

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        # features = torch.tensor(self.features[idx, :], dtype=torch.float)
        features = torch.tensor(self.features[idx, :].astype(float), dtype = torch.float32)
        label = torch.tensor(self.labels[idx].astype(float), dtype = torch.float32)

        return features, label

class PLSTestDataset(torch.utils.data.Dataset):
    def __init__(self, df):
        # Read the CSV file into a DataFrame
        columns_to_drop = ["start city name", "intermediate city name", "date", "start city coordinates", "intermediate city coordinates"]

        # Drop the specified columns
        df = df.drop(columns=columns_to_drop)

        #df = df.drop("risk_factor")
        self.features = df.to_numpy()

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        features = torch.tensor(self.features[idx, :].astype(float), dtype = torch.float32)
        return features

train_data = PLSDataset(df = normalized_training)
val_data = PLSDataset(df = normalized_val)
test_data = PLSTestDataset(df = normalized_test)
train_data.__getitem__(0)



# Define dataloaders for train, val and test datasets
# Dataloaders will yield a batch of frames and phonemes of given batch_size at every iteration



train_loader = torch.utils.data.DataLoader(
    dataset     = train_data,
    num_workers = 64,
    batch_size  = config['batch_size'],
    pin_memory  = True,
    shuffle     = True
)

val_loader = torch.utils.data.DataLoader(
    dataset     = val_data,
    num_workers = 12,
    batch_size  = config['batch_size'],
    pin_memory  = True,
    shuffle     = False
)

test_loader = torch.utils.data.DataLoader(
    dataset     = test_data,
    num_workers = 12,
    batch_size  = config['batch_size'],
    pin_memory  = True,
    shuffle     = False
)


print("Train dataset samples = {}, batches = {}".format(train_data.__len__(), len(train_loader)))
print("Validation dataset samples = {}, batches = {}".format(val_data.__len__(), len(val_loader)))
print("Test dataset samples = {}, batches = {}".format(test_data.__len__(), len(test_loader)))

# Testing code to check if your data loaders are working
for i, data in enumerate(train_loader):
    features, labels = data
    print(features.shape, labels.shape)
    break



import torch
class ResidualBlock(torch.nn.Module):
    def __init__(self, input_size):
        super(ResidualBlock, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, 10000)
        self.mish = torch.nn.Mish()
        self.fc2 = torch.nn.Linear(10000, input_size)

    def forward(self, x):
        residual = x
        out = self.mish(self.fc1(x))
        out = self.fc2(out)
        out += residual  # Add input to output
        out = self.mish(out)
        return out


class Serf(torch.nn.Module):
    def __init__(self):
        super(Serf, self).__init__()

    def forward(self, x):
        return x * torch.erf(F.softplus(x))

class GiantNetwork(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(GiantNetwork, self).__init__()

        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_size, 10000),
            torch.nn.BatchNorm1d(10000),
            torch.nn.Mish(),
            torch.nn.Dropout(p=0.5),

            ResidualBlock(10000),

            torch.nn.Linear(10000, 10000),
            torch.nn.BatchNorm1d(10000),
            torch.nn.Mish(),
            torch.nn.Dropout(p=0.5),

            # Residual blocks solve all problems

            ResidualBlock(10000),

            torch.nn.Linear(10000, 10000),
            torch.nn.BatchNorm1d(10000),
            torch.nn.Mish(),
            torch.nn.Dropout(p=0.5),

            ResidualBlock(10000),

            torch.nn.Linear(10000, 10000),
            torch.nn.BatchNorm1d(10000),
            torch.nn.Mish(),
            torch.nn.Dropout(p=0.5),

            torch.nn.Linear(10000, output_size),
            torch.nn.Mish(),
        )

    def forward(self, x):
        return self.net(x)


class MiniNet(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(MiniNet, self).__init__()

        self.net = torch.nn.Sequential(
            torch.nn.Linear(input_size, 2048),
            torch.nn.BatchNorm1d(2048),
            Serf(),
            torch.nn.Dropout(p=0.5),

            ResidualBlock(2048),

            torch.nn.Linear(2048, 1012),
            torch.nn.BatchNorm1d(1012),
            Serf(),
            torch.nn.Dropout(p=0.5),

            # Bottleneck residual block
            ResidualBlock(1012),

            torch.nn.Linear(1012, 1512),
            torch.nn.BatchNorm1d(1512),
            Serf(),
            torch.nn.Dropout(p=0.4),

            ResidualBlock(1512),

            torch.nn.Linear(1512, 2048),
            torch.nn.BatchNorm1d(2048),
            torch.nn.Mish(),
            torch.nn.Dropout(p=0.5),

            torch.nn.Linear(2048, output_size),
            torch.nn.Mish(),
        )

    def forward(self, x):
        return self.net(x)

input_size = features.shape[1]
model = MiniNet(input_size=input_size, output_size=1).to(device)


summary(model, (features.shape[1], ))

criterion = torch.nn.SmoothL1Loss()
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config['epochs'])

from torch.cuda.amp import autocast, GradScaler

def train(model, dataloader, optimizer, criterion):
    model.train()
    tloss, tacc = 0, 0
    batch_bar = tqdm(total=len(dataloader), dynamic_ncols=True, leave=False, position=0, desc='Train')

    for i, (frames, risk) in enumerate(dataloader):
        optimizer.zero_grad()

        frames = frames.to(device)
        risk = risk.to(device)

        logits = model(frames)
        loss = criterion(logits, risk)

        loss.backward()  # Scales the loss before backward pass
        optimizer.step()        # Unscale the gradients and update optimizer
        scheduler.step()

        tloss += loss.item()

        batch_bar.set_postfix(loss="{:.04f}".format(float(tloss / (i + 1))))
        batch_bar.update()

        del frames, risk, logits
        torch.cuda.empty_cache()

    batch_bar.close()
    tloss /= len(dataloader)

    return tloss

def eval(model, dataloader):

    model.eval() # set model in evaluation mode
    vloss, vacc = 0, 0 # Monitoring loss and accuracy
    batch_bar   = tqdm(total=len(val_loader), dynamic_ncols=True, position=0, leave=False, desc='Val')

    for i, (frames, risk) in enumerate(dataloader):

        ### Move data to device
        frames      = frames.to(device)
        risk    = risk.to(device)

        # makes sure that there are no gradients computed as we are not training the model now
        with torch.inference_mode():
            logits  = model(frames)
            loss    = criterion(logits, risk)

        vloss   += loss.item()
        batch_bar.set_postfix(loss="{:.04f}".format(float(vloss / (i + 1))))

        batch_bar.update()

        ### Release memory
        del frames, risk, logits
        torch.cuda.empty_cache()

    batch_bar.close()
    vloss   /= len(val_loader)

    return vloss

# Iterate over number of epochs to train and evaluate your model
for epoch in range(config['epochs']):

    print("\nEpoch {}/{}".format(epoch+1, config['epochs']))

    curr_lr                 = float(optimizer.param_groups[0]['lr'])
    train_loss   = train(model, train_loader, optimizer, criterion)
    val_loss       = eval(model, val_loader)

    print("\tTrain Loss {:.08f}\t Learning Rate {:.08f}".format(train_loss, curr_lr))
    print("\tVal Loss {:.08f}".format(val_loss))

def test(model, test_loader):
    model.eval()

    test_predictions = []

    with torch.inference_mode():

        for i, features in enumerate(tqdm(test_loader)):

            features   = features.to(device)

            logits  = model(features)
            logits = logits.cpu()

            test_predictions.extend(logits)

    return test_predictions

predictions = test(model, test_loader)
predictions

torch.save({'model_state_dict':model.state_dict(),
                  'optimizer_state_dict':optimizer.state_dict(),
                  'epoch': epoch}, './checkpoint.pth')

!ls -al

"""# Finetuning and Database

"""

"""
This is a prototype. Add persistent server for communication with a standard diffie hellmen keyexchange protocol or ssh key exchange.

Functionality: Allows future dynamic access of data from a database and tuning of the model based on this.

"""

def verify_database(API_KEY, VALID_KEY_LIST):
    if API_KEY in VALID_KEY_LIST:
        return True
    else:
        return False

def query_database(API_KEY, QUERY):
    csv_file_path = "/content/tuning.csv"  # CSV file path
    if verify_database(API_KEY, VALID_KEY_LIST):
        # Append QUERY data as a new row to the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([QUERY])  # Assuming QUERY is the data you want to append as a new row

        print(f"Data appended to {csv_file_path}.")
    else:
        print("Invalid API key. No changes made.")
        return None

# Example usage
API_KEY = "your_api_key_here"
VALID_KEY_LIST = ["valid_key_1", "valid_key_2", "your_api_key_here"]  # Include valid key
QUERY = "Example query result or data to append"

# Call the function with the necessary parameters
query_database(API_KEY, QUERY)

# Load Model
torch.load({'model_state_dict':model.state_dict(),
                  'optimizer_state_dict':optimizer.state_dict(),
                  'epoch': epoch}, './checkpoint.pth')


tuning_df = pd.read_csv("/content/tuning.csv")

tuning_data = PLSDataset(df = tuning_df)


# Preps a dataloader for tuning
tuning_loader = torch.utils.data.DataLoader(
    dataset     = tuning_data,
    num_workers = 4,
    batch_size  = config['batch_size'],
    pin_memory  = True,
    shuffle     = True
)


# Tune the model from uploaded server data
for epoch in range(config['epochs']):

    print("\nEpoch {}/{}".format(epoch+1, config['epochs']))

    curr_lr                 = float(optimizer.param_groups[0]['lr'])
    train_loss   = train(model, tuning_loader, optimizer, criterion)
    val_loss       = eval(model, val_loader)

    print("\tTrain Loss {:.08f}\t Learning Rate {:.08f}".format(train_loss, curr_lr))
    print("\tVal Loss {:.08f}".format(val_loss))