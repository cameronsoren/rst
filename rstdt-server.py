import socket
import struct
import threading

# Lookup tables for aggressive compression
PRICE_LOOKUP = [50, 100, 200, 300]  # 4 price ranges
RATING_LOOKUP = [1, 3, 4, 5]        # 4 rating levels
AMENITIES_LOOKUP = [0b0000, 0b1000, 0b1010, 0b1111]  # 4 binary patterns for amenities

SCHEMAS = {
    "hotels": {
        "fields": ["id", "price", "rating", "amenities"],
        "data": [
            {"id": 1, "price": 250, "rating": 5, "amenities": 0b1111},
            {"id": 2, "price": 150, "rating": 3, "amenities": 0b1010},
            {"id": 3, "price": 75,  "rating": 2, "amenities": 0b1000},
            {"id": 4, "price": 300, "rating": 4, "amenities": 0b1101},
            {"id": 5, "price": 350, "rating": 5, "amenities": 0b1111},
        ]
    }
}

# Map actual price, rating, amenities to indices
def get_price_index(price):
    for i, p in enumerate(PRICE_LOOKUP):
        if price <= p:
            return i
    return len(PRICE_LOOKUP) - 1  # max index if out of range

def get_rating_index(rating):
    for i, r in enumerate(RATING_LOOKUP):
        if rating == r:
            return i
    return 0  # default index if not found

def get_amenities_index(amenities):
    for i, a in enumerate(AMENITIES_LOOKUP):
        if amenities == a:
            return i
    return 0  # default index

def bitpack_entry_optimized(entry):
    price_index = get_price_index(entry["price"])
    rating_index = get_rating_index(entry["rating"])
    amenities_index = get_amenities_index(entry["amenities"])

    # Pack the entry into 9 bits
    packed_data = (entry["id"] << 6) | (price_index << 4) | (rating_index << 2) | amenities_index
    print(f"Packing optimized entry: {entry} into bits: {bin(packed_data)}")
    return packed_data

def handle_search(resource_name, price_min, price_max):
    if resource_name not in SCHEMAS:
        return []
    
    data = SCHEMAS[resource_name]["data"]
    return [entry for entry in data if price_min <= entry['price'] <= price_max]

def handle_client(client_socket):
    try:
        while True:
            header = client_socket.recv(1)
            if not header:
                break
            
            header_bits = struct.unpack('!B', header)[0]
            op_code = (header_bits >> 5) & 0b111
            resource_id = (header_bits >> 2) & 0b111

            resource_name = list(SCHEMAS.keys())[resource_id] if resource_id < len(SCHEMAS) else None
            print(f"Received op_code: {op_code}, resource_id: {resource_id}, resource: {resource_name}")

            if resource_name and op_code == 0:
                price_range = client_socket.recv(4)
                price_min, price_max = struct.unpack('!HH', price_range)
                print(f"Received price_min={price_min}, price_max={price_max} for {resource_name}")
                results = handle_search(resource_name, price_min, price_max)

                # Pack response with 9 bits per entry
                response = b""
                for entry in results:
                    packed_entry = bitpack_entry_optimized(entry)
                    response += struct.pack('!H', packed_entry)  # Use 2 bytes to send 9-bit packed entry

                client_socket.send(struct.pack('!H', len(response)) + response)
                print(f"Sent response: {response.hex()}")
            else:
                client_socket.send(struct.pack('!H', 0))
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Highly Compressed RSTDT Server running...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()


