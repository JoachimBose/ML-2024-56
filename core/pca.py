#https://www.kaggle.com/code/pmmilewski/pca-decomposition-and-keras-neural-network/notebook
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pandas import read_csv, DataFrame
import matplotlib.pyplot as plt
from numpy import cumsum, savetxt, dtype
from core.main.config import OUTPUT_DIR

# Where to read the source data from, where to put the output, how many components to get, and the label of the target value
source_location = OUTPUT_DIR + "dataset.csv"
target_location = OUTPUT_DIR + "output.csv"
n_components = 10
target = "target-size"
test = "test"

# Load the data and separate out the target
data = read_csv(source_location)
Y_data = data[target].values.astype("int32")
test_data = data[test].values
data.drop([target, test], axis=1, inplace=True)

X_data = (data.values).astype("float32")
scaler = StandardScaler()
scaler.fit(X_data)
X_sc_data = scaler.transform(X_data)

# Create a object for PCA and transform the data using the PCA
pca = PCA(n_components=n_components)
# If we want to scale the inputs use X_sc_train
X_pca_data = pca.fit_transform(X_data)

# Plot the variance to see how it scales with the number of components
plt.plot(cumsum(pca.explained_variance_ratio_))
plt.savefig("img")

# Create a dataframe, add the target label and dump it back to disk
df = DataFrame(X_pca_data)
df.insert(len(df.columns), target, Y_data, True)
df.insert(len(df.columns), test, test_data, True)

fmt = ""
for col in df:
    if(type(df[col].dtype) == dtype('object')):
        fmt += "%s,"
    else:
        fmt += "%.18e,"
fmt = fmt[:-1] 
savetxt(target_location, df, delimiter=",", fmt=fmt)

