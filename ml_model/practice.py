import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.compose import ColumnTransformer #it help applying change to the data_set obj ,changes which are made by the encoder
import warnings
warnings.filterwarnings('ignore')


#initializing thee data to variable so we can work on it 
data=pd.read_csv('smart_shop_sales.csv')
print("data initialization success")

#exploring the data
data.describe()
a=data.describe()  #give the data like  min max etc about the  numberic data in the table

data.isnull().sum()

#columns
#Item_Identifier,Item_Weight,Item_Fat_Content,Item_Visibility,Item_Type
#Item_MRP,Outlet_Identifier,Outlet_Establishment_Year,Outlet_Size
#Outlet_Location_Type,Outlet_Type,Item_Outlet_Sales


#cleaning the null value 
#1.identify the catorical data in the row
data['Item_Identifier'].unique()
data['Item_Identifier'].nunique()  #as the data cant be helpful in model training so discard it

#moving to Item_Weight

data['Item_Weight'].unique()
data['Item_Weight'].nunique()

data['Item_Weight'].isnull().sum() #so there are 1463 col which are null solving them

#using seaborn to analyse the column and identfying pattern
sns.histplot(data['Item_Weight'])
#to recoganise pattern drae distplot
sns.distplot(data['Item_Weight'])
#as there is bell curve so we will use mean to replace the value 

#replacing the value
data['Item_Weight']=data['Item_Weight'].fillna(data['Item_Weight'].mean())
print("changed")

#done with this column


#woking with Item_Fat_Content
#searching for the category 
data['Item_Fat_Content'].unique()  
data['Item_Fat_Content'].value_counts() #multiple column with same name so making them same writing a fucntion

def col_rename(x):
    if x=='LF' or x== 'low fat':
        return 'Low Fat'
    elif x== 'reg':
        return 'Regular'
    else:
        return x
#calling the function 
data['Item_Fat_Content']=data['Item_Fat_Content'].apply(col_rename)

data['Item_Fat_Content'].value_counts()

data.info()
data.isnull().sum()

#now moving onto the Outlet_Size as it have soo many nulls init
data['Outlet_Size'].unique()

#analyzing the data as which category is at median (most occuring)
sns.histplot(data['Outlet_Size'])
plt.show()
#as the frequency of medium is highest so we will put it to the nan values in the data_Set
data['Outlet_Size'].fillna('Medium',inplace=True)
#done with this one 



#deleting the unwanted columns from the table which are note required for the model training
data.drop(['Item_Identifier','Outlet_Establishment_Year','Outlet_Identifier'],axis=1,inplace=True)




# applying label and one hot enoding to the columns 
#1. identifying the columns which need the one hot or label 
#columns of label encoding (can be ordered)-- Item_Fat_Content,Outlet_Size,Outlet_Location_Type

#creating the object of each row for the label encoding  and then applying the functin

le_fat_content=LabelEncoder() 
le_size=LabelEncoder()
le_location=LabelEncoder()

#starting the encoding process 
data['Item_Fat_Content']=le_fat_content.fit_transform(data['Item_Fat_Content'])
data['Outlet_Size']=le_size.fit_transform(data['Outlet_Size'])
data['Outlet_Location_Type']=le_location.fit_transform(data['Outlet_Location_Type'])

#now the data is label encoded moving the one hot encoding for which we will use
#columns (these cant be ordered)-- Item_Type,Outlet_Type

#for one hot encoding create the list of the columns
oh_cols=['Item_Type','Outlet_Type']

oh_data_ppros=ColumnTransformer(
    [('onehotencoder',OneHotEncoder(sparse_output=False,handle_unknown='ignore'),oh_cols)]
    )

data=oh_data_ppros.fit_transform(data)



