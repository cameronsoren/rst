
# rst (radically simplified transfer)

rst is an experimental ultra-compressed version of REST protocol designed for environments with extreme constraints on bandwidth, power, and reliability. Its primary goal is to reduce data transfer and processing overhead by utilizing bit-packed commands and responses. This makes rst suitable for edge computing, low-power IoT devices, disaster recovery networks, and deep space communications.

## Features

- **Ultra Compression:** Bit-packed commands and responses allow minimal data transfer.
- **Dynamic Resource Registration:** Developers can define new resources and fields at runtime.
- **Apocalyptic API Design:** Optimized for environments where communication and power reliability is scarce.
- **Aggressive Optimization:** Prioritizes raw efficiency through bit-level compression beyond traditional lightweight protocols like CoAP.

## Potential Use Cases

- **Edge IoT Networks:** Efficient communication for devices with limited power or bandwidth.
- **Disaster Zones:** Networks with unreliable connections that need to self-organize.
- **Space Exploration:** Communications in deep space, where bandwidth is a premium.
- **Low-Power Spyware:** Devices that need to execute complex tasks or retrieve data with minimal power usage.

## Proof of Concept: Booking a Hotel on Mars

To showcase the rst protocol in action, the Proof of Concept (PoC) involves a task: searching for hotels and retrieving results.

### Compression Comparison

- **Uncompressed Size (JSON):** ~350 bytes
- **Compressed Size (bit-packed rst):** ~10 bytes
- **Compression Ratio:** 97%

### Example Features in the PoC

- **Price Lookup:** Predefined price ranges are bit-packed for optimal transfer.
- **Rating Lookup:** Ratings are mapped to binary for minimal space usage.
- **Amenities Lookup:** Amenities represented in a highly compressed bit format.

## How It Works

The rst protocol operates by utilizing lookup tables for various fields, such as price, ratings, and amenities. This allows for aggressive compression, as each field is mapped to a binary representation and packed into as few bits as possible. Commands are sent using minimalistic headers and payloads, and the server unpacks and processes the bit-packed data.

### Server Architecture

- The server listens for client connections.
- It receives compressed data packets, unpacks them, processes the search queries, and sends bit-packed responses.

### Client Architecture

- The client sends a compressed search request.
- It then receives a compressed response, which it unpacks and processes to display results.

## Installation

To run the PoC:

1. Clone the repository.
2. Install the required Python dependencies.
3. Run the server:
   ```
   python server.py
   ```
4. Run the client:
   ```
   python client.py
   ```

## License

This project is licensed under the MIT License.

