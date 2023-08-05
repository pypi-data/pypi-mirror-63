# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_core.ipynb (unless otherwise specified).

__all__ = []

# Cell
from fastai.tabular import *

# Cell
def _dataframe_of_dl(dl, col_names):
    "Takes a dataloader and column names and returns all of its content converted to a single dataframe."
    # for all elements in dataloader, get cont and cat columns, converts them to numpy, concat them
    matrix = [np.concatenate([x[0].to('cpu').numpy(), x[1].to('cpu').numpy()], axis=1) for x,y in iter(dl)]
    # concats all the rows before converting the result into a dataframe
    df = pd.DataFrame(np.concatenate(matrix), columns=col_names)
    return df

# Cell
def _prepare_data(learn:Learner, test_data:DataFrame=None, n_samples:int=128):
  "Prepares train and test data for `SHAP`, pass in a learner with optional data"
  col_names = learn.data.col_names
  if test_data is None:
    # we use the validation dataset as test set
    if learn.data.valid_dl is None: raise Exception("Error: you tried to use Shap with neither valid dataset nor user defined test data. Please pass a dataframe to test_data")
    X_test = _dataframe_of_dl(learn.data.valid_dl, col_names)
    X_test = X_test.sample(min(n_samples, len(X_test)))
  else:
    # converts test_data dataframe to a processed tabular list
    test_data = TabularList.from_df(test_data, cat_names=learn.data.cat_names, cont_names=learn.data.cont_names, procs=learn.data.procs)
    # temporary adds test_data as a test dl to be able to turn it into a properly formated dataframe
    if learn.data.test_dl is not None: print("Warning: this function will erase the current test dataset!")
    learn.data.add_test(test_data)
    X_test = _dataframe_of_dl(learn.data.test_dl, col_names)
    learn.data.test_dl = None
  X_train = _dataframe_of_dl(learn.data.train_dl, col_names)
  return X_train, X_test

# Cell
def _predict(learn:Learner, data:pd.DataFrame):
  "Predict function for some data on a fastai model"
  device = 'cuda' if torch.cuda.is_available() else 'cpu'
  model = learn.model.to(device)
  nb_cat_cols = len(learn.data.train_ds.x.cat_names)
  nb_cont_cols = len(learn.data.train_ds.x.cont_names)
  x_cat = torch.from_numpy(data[:, :nb_cat_cols]).to(device, torch.int64)
  x_cont = torch.from_numpy(data[:, -nb_cont_cols:]).to(device, torch.float32)
  with torch.no_grad():
    pred_probs = learn.model(x_cat, x_cont).cpu().numpy() # .detach().to('cpu').numpy()
  return pred_probs