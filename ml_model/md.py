import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from lazypredict.Supervised import LazyRegressor

#this will ignore all the warnings 
import warnings
warnings.filterwarnings('ignore')


smart_shop_data= pd.read_csv("smart_shop_sales.csv")
print("code till here executed")

#to find no of rows and column in the data set 
smart_shop_data.shape
#to get this in tabulated form intialize it to the variable
aa=smart_shop_data.shape


#to get rows mean,min,max of the integer columns 
smart_shop_data.describe()
#for better understand initialize it to the variable
a=smart_shop_data.describe()

#to check if null value are there in the data
smart_shop_data.isnull()
#for better understand we can do sum for it 
smart_shop_data.isnull().sum()

smart_shop_data.info

#15 monday codes 

#finding unique value in the specific column 
smart_shop_data['Item_Weight'].unique()
smart_shop_data['Item_Weight'].nunique()

smart_shop_data['Outlet_Size'].unique()
smart_shop_data['Outlet_Size'].nunique()

#clearing the null value and clearing it with the mean as per the analysis it has the bell curve
sns.histplot(smart_shop_data['Outlet_Size']) #so we will file the null with medium as most occuring in non numeric data
plt.show()
#same for the item weight fields 
#filling the data
smart_shop_data['Outlet_Size'].fillna('Medium',inplace=True)


sns.histplot(smart_shop_data['Item_Weight'])
plt.show()
sns.distplot(smart_shop_data['Item_Weight'])  #only work with numeric data
plt.show()   #so as it makes the bell curve we will fiel the null with mean
#filling with mean 

smart_shop_data['Item_Weight'].fillna(smart_shop_data['Item_Weight'].mean(),inplace=True)

#checking for the data

smart_shop_data['Item_Identifier'].value_counts() #as there is no requirement of the coulumn so we will drop the column 

smart_shop_data['Item_Fat_Content'].value_counts() #now theere are columns where the data is same eg reg and regular low fat lf and LowFat

def change_same_value(x):
    if x=='low fat' or x=='LF':
        return 'Low Fat'
    elif x=='reg':
        return 'Regular'
    else:
        return x

#calling this function to apply chnage to the field 
smart_shop_data["Item_Fat_Content"]=smart_shop_data['Item_Fat_Content'].apply(change_same_value)

smart_shop_data['Item_Fat_Content'].value_counts()






#starting work to work on the rest of columns form here self work
#Item_Visibility,Item_Type
#Item_MRP,Outlet_Identifier,Outlet_Establishment_Year,Outlet_Size
#Outlet_Location_Type,Outlet_Type,Item_Outlet_Sales

#Item_Visibility
smart_shop_data['Item_Visibility'].describe()
smart_shop_data['Item_Visibility'].unique()
smart_shop_data['Item_Visibility'].nunique()

smart_shop_data['Item_Visibility'].isnull().sum()
#since there are no null value nothing to be changed here 

# woking for the Item_Type

smart_shop_data['Item_Type'].describe()
smart_shop_data['Item_Type'].unique()
smart_shop_data['Item_Type'].nunique()
smart_shop_data['Item_Type'].value_counts() #finding category
smart_shop_data['Item_Type'].isnull().sum()  #no null so okk

#no correction is needed in this column 

#working with Item_MRP
smart_shop_data['Item_MRP'].value_counts() # no category can be formed multiple prices 
smart_shop_data['Item_MRP'].isnull().sum() #no null values

#no correctinos needed
smart_shop_data['Outlet_Identifier'].value_counts()
smart_shop_data['Outlet_Identifier'].isnull().sum()

#no null value are here so no correction needed 



#working with Outlet_Establishment_Year
smart_shop_data['Outlet_Establishment_Year'].value_counts() 

#no need for the coulumn as it does not determine anything


#working with Outlet_Size
smart_shop_data['Outlet_Size'].value_counts() 
smart_shop_data['Outlet_Size'].isnull().sum() #so there are 2410 null solving them 

sns.histplot(smart_shop_data['Outlet_Size'])
plt.show()

#so most occuring is medium as per the graph so we will replace the null value with medium
smart_shop_data['Outlet_Size'].fillna('Medium',inplace=True)

#working with Outlet_Location_Type
smart_shop_data['Outlet_Location_Type'].value_counts() #can be arranged categorically
smart_shop_data['Outlet_Location_Type'].isnull().sum() #no null

#working with Outlet_Type
smart_shop_data['Outlet_Type'].value_counts() #category of city
smart_shop_data['Outlet_Type'].isnull().sum() #no null

#working with Item_Outlet_Sales
smart_shop_data['Item_Outlet_Sales'].value_counts()  #these are sales record
smart_shop_data['Item_Outlet_Sales'].nunique() #these are sales record
smart_shop_data['Item_Outlet_Sales'].isnull().sum() #no null value


#starting with the practice on ml 17 june 
smart_shop_data.drop(['Item_Identifier','Outlet_Identifier','Outlet_Establishment_Year'],axis=1,inplace=True)  #axis=1 is for deleting column and axis =0 for rows which is also by default

data_info=smart_shop_data.info()   

#starting to label encoding start with creating objects 

le_fat_content=LabelEncoder() #for fat content row obj
le_size=LabelEncoder()
le_type=LabelEncoder()

#converting the data in row 
smart_shop_data['Item_Fat_Content']=le_fat_content.fit_transform(smart_shop_data['Item_Fat_Content'])
smart_shop_data['Outlet_Size']=le_size.fit_transform(smart_shop_data['Outlet_Size'])
smart_shop_data['Outlet_Location_Type']=le_type.fit_transform(smart_shop_data['Outlet_Location_Type'])




x=smart_shop_data.drop(['Item_Outlet_Sales'],axis=1)    #taki hamari x axis me target yani ki Item_Outlet_Sales hat jaye
y=smart_shop_data['Item_Outlet_Sales']   #y hamara target column hota hai so ham Item_Outlet_Sales ko target column bna denge jo ml predict karega hamare lia


#performing the one hot encoding on the other columns
#using column transformer to call the one hot encoder
x.columns
categorical_columns=['Item_Type','Outlet_Type']
numerical_Column=['Item_Weight','Item_Fat_Content','Item_Visibility','Item_MRP','Outlet_Size',
                  'Outlet_Location_Type']

preprocessor=ColumnTransformer(
    [('onehotencoder',OneHotEncoder(sparse_output=False,handle_unknown='ignore'),categorical_columns), #handle_unknow is used to ignore the new unidetified value in the future
    
    ('standardscaler',StandardScaler(),numerical_Column)]
    )
x=preprocessor.fit_transform(x)

#splitting the data 
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=100) #random_state is used to justify the starting row of the data 

#linear regressor 
model_lr=LinearRegression()
model_lr.fit(x_train,y_train)
y_predict=model_lr.predict(x_test)
r_score=r2_score(y_test,y_predict)

#decison tree
model_dtr=DecisionTreeRegressor()
model_dtr.fit(x_train,y_train)
y_predict_dtr=model_dtr.predict(x_test)
r_score_dtr=r2_score(y_test,y_predict_dtr)

#random forest 
model_rfr=RandomForestRegressor()
model_rfr.fit(x_train,y_train)
y_predict_rfr=model_rfr.predict(x_test)
r_score_rfr=r2_score(y_test,y_predict_rfr)

#lazy predict 
model_lazy=LazyRegressor()
model,prediction=model_lazy.fit(x_train,x_test,y_train,y_test)

#putting these value into the variable using joblib to store them into the local machine
joblib.dump(le_fat_content,'le_fat_content.joblib')
joblib.dump(le_size,'le_size.joblib')
joblib.dump(le_type,'le_type.joblib')

#preprocessor
joblib.dump(preprocessor,'preprocessor.joblib')

#model used random forest
joblib.dump(model_rfr,'model_rfr.joblib')






