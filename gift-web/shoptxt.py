import requests
import json

def get_shop_items():
    # Send GET request to the API
    url = "https://api.rookie-spitfire.xyz/v1/epic/shop"
    try:
        response = requests.get(url, verify=False)  # Added verify=False for SSL issues
        response.raise_for_status()
        
        data = response.json()
        offers = data['data']['offers']
        
        # Create a formatted string with numbered items
        formatted_items = []
        item_number = 1  # Separate counter for displayed items
        
        for offer in offers:
            try:
                # Get name from different possible locations
                name = offer.get('name') or offer.get('devName', 'Unknown Item')
                
                # Skip if [VIRTUAL] is in the name or devName
                if "[VIRTUAL]" in name:
                    continue
                
                # Get ID
                item_id = offer.get('id', 'Unknown ID')
                
                # Get price
                price = offer.get('price', {}).get('final', 0)
                
                # Format item info
                item_info = f"{item_number}. {name} - {price} V-Bucks"
                formatted_items.append(item_info)
                item_number += 1  # Increment only for non-virtual items
                
            except Exception as e:
                print(f"Error processing offer: {str(e)}")
                continue
        
        # Join all items with newlines
        all_items = "\n".join(formatted_items)
        
        # Save to file
        with open("shop.txt", "w", encoding="utf-8") as f:
            f.write(all_items)
            
        return all_items
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching shop data: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    print(get_shop_items())