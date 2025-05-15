from collections import defaultdict

class MemoryCart:
    def __init__(self):
        self._cart = defaultdict(list)

    def add_item(self, user_id: int, item: dict):
        cart = self._cart[user_id]
        for i in cart:
            if i['product_id'] == item['product_id']:
                i['quantity'] += item.get('quantity', 1)
                return
            
        self._cart[user_id].append(item)
        
    def get_cart(self, user_id: int):
        return self._cart[user_id]
    
    def clear_cart(self, user_id: int):
        self._cart[user_id] = []

    def remove_item(self, user_id: int, product_id: int):
        self._cart[user_id] = [i for i in self._cart[user_id] if i['product_id'] != product_id]
