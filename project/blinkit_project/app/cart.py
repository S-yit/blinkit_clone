from blinkit_project import setting
class cart(object):
    def _init_(self,request):
        self.session=request.session
        cart=self.session.get(setting.CARt_SESSION_ID)
        print(cart)
        if not cart:
            cart=self.session[setting.CARt_SESSION_ID]={}
        self.cart=cart
        print(self.cart)
    def get_cart_items_list(self):
        pet_ids = self.cart.keys()
        pets=pet.object.filter(id__in=pet_ids)
        
        cart=self.cart.copy()
        print(cart is self.cart)
        for pet in pets:
            cart[str(pet.id)]['pet']=pet
        
        items_list=[]
        for item in cart.values():
            item['price']=float(item['price'])
            item['total_price']=item['price']*item['quantity']
            items_list.append(item)
            print('item: ',item)

        print("get_cart_item_listself.cart",self.cart)
        print("get_cart_items_listself cart",cart)
        return items_list
    
    def get_cart_items_count(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self,pet,quantity=1,update_quantity=False):
        print(self.cart)
        pet_id=str(pet.id)
        if pet_id not in self.cart:
            self.cart[pet_id]={'quantity': 0,'price': str(pet)}
        if update_quantity:
            self.cart[pet_id]['quantity']= quantity
        else:
            self.cart[pet_id]['quantity'] += quantity
        print(self.cart)
        if 'pet' in self.cart:
            self.cart.pop('pet')
        if 'total_price' in self.cart:
            self.cart.pop('total_price')