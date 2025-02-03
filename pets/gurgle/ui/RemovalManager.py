class RemovalManager:
    def __init__(self):
        self.tracked_items = {}
    
    def add_item(self, group, element, time_to_live, current_time):

        item_id = id(element) 
        self.tracked_items[item_id] = {
            "group": group,
            "element": element,
            "expire_time": current_time + time_to_live,
            "current_time": current_time
        }
        
    def update(self, current_time):
     
        items_to_remove = []
        
        for item_id, item_data in self.tracked_items.items():
            if current_time >= item_data["expire_time"]:
                try:
                    if item_data["element"] in item_data["group"]:
                        item_data["group"].remove(item_data["element"])
                except (ValueError, KeyError) as e:
                    print(f"Warning: Could not remove element - {e}")
                items_to_remove.append(item_id)
        
        # Clean up tracked items
        for item_id in items_to_remove:
            del self.tracked_items[item_id]