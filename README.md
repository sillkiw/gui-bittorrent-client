# Torrent Client with GUI

This project is a basic implementation of a Torrent Client with GUI. The client connects to torrent trackers, discovers peers, downloads files in pieces, and assembles them, following the fundamentals of the BitTorrent protocol. This project demonstrates concepts of peer-to-peer (P2P) networking, file handling, and asynchronous data exchange in Python .

## Features

- **Torrent File Parsing**: Reads and extracts metadata and tracker information from `.torrent` files.
- **Tracker Communication**: Connects with torrent trackers to retrieve lists of peers.
- **Peer Discovery and Connection**: Connects with peers and maintains active connections to download data.
- **Piece-wise Downloading**: Downloads files piece by piece from multiple peers, increasing efficiency.
- **Piece Verification**: Validates downloaded pieces against hash checks to ensure data integrity.
- **File Assembly**: Reassembles downloaded pieces into the original file.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- The required Python packages are listed in `req.txt`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sillkiw/TorrentClientProjectCourse.git
   cd TorrentClientProjectCourse

2. Install dependencies:
    ```bash
    pip install -r req.txt
    
### Usage 
Just run head_interface.py and you will meet with GUI

### Acknowledgments
This project drew inspiration and referenced code from https://github.com/gallexis/PyTorrent by gallexis.
