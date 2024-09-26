import socket
import struct

# Lookup tables for decompressing
PRICE_LOOKUP = [50, 100, 200, 300]  # 4 price ranges
RATING_LOOKUP = [1, 3, 4, 5]        # 4 rating levels
AMENITIES_LOOKUP = [0b0000, 0b1000, 0b1010, 0b1111]  # 4 binary patterns for amenities

def bitunpack_entry_optimized(packed_data):
    # Unpack the 9-bit data into ID, price, rating, and amenities using lookup tables
    hotel_id = (packed_data >> 6) & 0b111  # 3 bits for hotel ID
    price_index = (packed_data >> 4) & 0b11  # 2 bits for price
    rating_index = (packed_data >> 2) & 0b11  # 2 bits for rating
    amenities_index = packed_data & 0b11  # 2 bits for amenities

    return {
        "id": hotel_id,
        "price": PRICE_LOOKUP[price_index],
        "rating": RATING_LOOKUP[rating_index],
        "amenities": AMENITIES_LOOKUP[amenities_index]
    }

def send_search_request(sock, op_code, resource_id, price_min, price_max):
    header = (op_code << 5) | (resource_id << 2)
    request = struct.pack('!B', header) + struct.pack('!HH', price_min, price_max)

    print(f"Sending search request: {price_min} - {price_max} for resource {resource_id}")
    sock.send(request)

    # Receive the response length
    response_length = struct.unpack('!H', sock.recv(2))[0]
    print(f"Received response length: {response_length}")

    # Receive the response and unpack
    response = sock.recv(response_length)
    entries = []
    for i in range(0, len(response), 2):  # Each entry is packed into 2 bytes (16 bits)
        packed_entry = struct.unpack('!H', response[i:i + 2])[0]
        entry = bitunpack_entry_optimized(packed_entry)
        entries.append(entry)

    return entries

def print_entries(entries):
    for entry in entries:
        print(f"ID: {entry['id']}, Price: ${entry['price']}, Rating: {entry['rating']}/5, Amenities: {bin(entry['amenities'])}")

def tcp_compressed_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 9999))

        # Search for hotels
        print("\nSearching for hotels between $100 and $300...")
        hotels = send_search_request(sock, 0, 0, 100, 300)  # 0: SEARCH, 0: /hotels
        print("Search Results for Hotels:")
        print_entries(hotels)

if __name__ == "__main__":
    tcp_compressed_client()
