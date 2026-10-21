from django.shortcuts import render
from .models import SmartShopSales,history
import pandas as pd

# Create your views here.
def dashboard(request):
    sales_cost=123456
    sales_data=SmartShopSales.objects.all().values_list('Item_Outlet_Sales',flat=True)
    print(sales_data)
    sales_data=[float(i) for i in sales_data]
    total_sales=round(sum(sales_data))
    sales_count=len(sales_data) #to calculate total count 


    #calculating tier average sales 
    tier_count=SmartShopSales.objects.all().values_list('Outlet_Location_Type',flat=True).distinct()  #this will get the total no of tier like here we have 3 tiers 
    print(tier_count)
    #finding the avg  sales 
    tier_count=len(tier_count)
    if tier_count > 0:
        avg_tier_count=round(total_sales/tier_count)
    else:
        avg_tier_count=0
    #count no of item 
    item_count=SmartShopSales.objects.all().values_list('Item_Type',flat=True).distinct()
    print(item_count)
    item_count=len(item_count)

     #calculating tier data
    #tier 1 city  sales
    tier_1_count=SmartShopSales.objects.filter(Outlet_Location_Type='Tier 1').values_list('Item_Outlet_Sales',flat=True)
    print(tier_1_count)
    tier_1_count=[float(i) for i in tier_1_count]
    sales_tier_1_count=round(sum(tier_1_count))
    #do similar for tier 2 and tier 3 H.W.S

    #tier 2 sales
    tier_2_count=SmartShopSales.objects.filter(Outlet_Location_Type='Tier 2').values_list('Item_Outlet_Sales',flat=True)
    print(tier_2_count)
    tier_2_count=[float(i) for i in tier_2_count]
    sales_tier_2_count=round(sum(tier_2_count))

    #tier 3 sales
    tier_3_count=SmartShopSales.objects.filter(Outlet_Location_Type='Tier 3').values_list('Item_Outlet_Sales',flat=True)
    print(tier_3_count)
    tier_3_count=[float(i) for i in tier_3_count]
    sales_tier_3_count=round(sum(tier_3_count))

    #pie char data calculating (to find per prodduct sales count)
    distinct_item_type=SmartShopSales.objects.all().values_list('Item_Type',flat=True).distinct()
    #making list 
    dict_count={} #this is empty dictionary to store the value of counts 
    for i in distinct_item_type:
        data=SmartShopSales.objects.filter(Item_Type=i).values_list('Item_Type',flat=True)  #this will compare the list item to the DB column for the number of time iteration 
        dict_count[i]=len(data)
    print(dict_count)

    return render(request,'dashboard.html',{'total_sales':total_sales,
                                            'sales_count':sales_count,
                                            'avg_tier_count':avg_tier_count,
                                            'item_count':item_count,
                                            'sales_tier_1_count':sales_tier_1_count,
                                            'sales_tier_2_count':sales_tier_2_count,
                                            'sales_tier_3_count':sales_tier_3_count,
                                            'dict_count':dict_count})

   





    # sales_data=pd.read_csv('E:\smart_shop_sales\ml_model\smart_shop_sales.csv')
    # for i,j in sales_data.iterrows():
    #     print(i,j)
    #     SmartShopSales.objects.create(
    #         Item_Identifier=j['Item_Identifier'],
    #         Item_Weight=j['Item_Weight'],
    #         Item_Fat_Content=j['Item_Fat_Content'],
    #         Item_Visibility=j['Item_Visibility'],
    #         Item_Type=j['Item_Type'],
    #         Item_MRP=j['Item_MRP'],
    #         Outlet_Identifier=j['Outlet_Identifier'],
    #         Outlet_Establishment_Year=j['Outlet_Establishment_Year'],
    #         Outlet_Size=j['Outlet_Size'],
    #         Outlet_Location_Type=j['Outlet_Location_Type'],
    #         Outlet_Type=j['Outlet_Type'],
    #         Item_Outlet_Sales=j['Item_Outlet_Sales'],
    # )
    

def History(request):
    data=history.objects.all().values()   #any quesry to be runned also here 
    return  render(request,'history.html',{'historical_Data':data})  
    #this will give the data in key value pair so whenever we refer to the data_hist the html page will show the data 



def AI_Recommendation(request):
    import joblib

    sales=None #to sore and display the final result

    if request.method=='POST':
        print(request.POST)
        le_fat_content=joblib.load('ml_model/le_fat_content.joblib')
        le_size=joblib.load('ml_model/le_size.joblib')
        le_type=joblib.load('ml_model/le_type.joblib')

        preprocessor=joblib.load('ml_model/preprocessor.joblib')
        model_rfr=joblib.load('ml_model/model_rfr.joblib')

        data=pd.DataFrame([request.POST.dict()])
        #droping the crrf token column 
        data.drop(['csrfmiddlewaretoken'],axis=1,inplace=True)
        print(data)

        data['Item_Fat_Content']=le_fat_content.transform(data['Item_Fat_Content'])
        data['Outlet_Size']=le_size.transform(data['Outlet_Size'])
        data['Outlet_Location_Type']=le_type.transform(data['Outlet_Location_Type'])
        data=preprocessor.transform(data)

        print(data)
        sales = model_rfr.predict(data)
        sales =sales[0]
        print(sales)

        Item_Weight=request.POST.get('Item_Weight')   #it will strore the input to store in the history table 
        Item_Fat_Content=request.POST.get('Item_Fat_Content')
        Item_Visibility=request.POST.get('Item_Visibility')
        Item_Type=request.POST.get('Item_Type')
        Item_MRP=request.POST.get('Item_MRP')
        Outlet_Size=request.POST.get('Outlet_Size')
        Outlet_Location_Type=request.POST.get('Outlet_Location_Type')
        Outlet_Type=request.POST.get('Outlet_Type')
    

        history.objects.create(Item_Weight=Item_Weight,
                               Item_Fat_Content=Item_Fat_Content,
                               Item_Visibility=Item_Visibility,
                               Item_Type=Item_Type,
                               Item_MRP=Item_MRP,
                               Outlet_Size=Outlet_Size,
                               Outlet_Location_Type=Outlet_Location_Type,
                               Outlet_Type=Outlet_Type,
                               Item_Outlet_Sales=sales)

        print(history.objects.count())
#showing this data to the html page the  history page 
    print(request.POST)
    return render(request,'ai_recomendation.html',  #this will return the main result to the variable and shown to the main popup 
                  {
                      'y_pred':round(sales,2) if sales else None,    #this is done for diplaying the result to the page popup widget
                      'form_data':request.POST if request.method == 'POST' else{}
                  })
  

#SmartShopSales.objects.all().delete() #this command will delete all out data

