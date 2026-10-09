# LandChain --- Blockchain-Based Land Registry System

LandChain is an academic prototype demonstrating how blockchain concepts
can support transparent, traceable digital land-record management. It
provides a web interface for land registration, ownership-transfer
history, blockchain integrity verification, record search, and digital
ownership certificates.

> **Project status:** Educational prototype. This version uses a custom
> Python blockchain, SHA-256 hashing, and JSON file persistence. It is
> not connected to Ethereum, does not currently use Solidity smart
> contracts or MetaMask, and is not a legally authoritative land
> registry.

## Table of Contents

-   [Overview](#overview)
-   [Problem Statement](#problem-statement)
-   [Objectives](#objectives)
-   [Features](#features)
-   [Technology Stack](#technology-stack)
-   [How It Works](#how-it-works)
-   [Architecture](#architecture)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Run the Application](#run-the-application)
-   [Using LandChain](#using-landchain)
-   [Blockchain Design](#blockchain-design)
-   [Limitations and Security](#limitations-and-security)
-   [Testing](#testing)
-   [Future Scope](#future-scope)
-   [Contributing](#contributing)
-   [Disclaimer](#disclaimer)
-   [License](#license)

## Overview

Land records are important documents used to record property details and
ownership. LandChain explores how a hash-linked ledger and a simple web
interface can make record history easier to inspect and integrity checks
easier to demonstrate.

## Problem Statement

Record-management workflows may involve manual processes, fragmented
records, and limited visibility into historical changes. This project
demonstrates a basic digital workflow where registration and transfer
events are stored in a hash-linked ledger. It does not replace official
land records, legal checks, or government systems.

## Objectives

-   Build a simple web interface for sample land records.
-   Record registration and ownership-transfer events.
-   Maintain chronological transaction history.
-   Use SHA-256 hashes to help detect changes to block contents.
-   Link blocks through previous-block hashes.
-   Provide chain-integrity verification.
-   Search and inspect land records.
-   Demonstrate Python, Flask, frontend development, and blockchain
    fundamentals.

## Features

-   **Land registration:** Store land ID, owner, location, area, and
    survey number.
-   **Ownership transfer:** Add a transfer event while preserving
    earlier history.
-   **Record search:** Find land records through the available search or
    verification page.
-   **Blockchain explorer:** Inspect blocks, transaction data,
    timestamps, and hashes.
-   **Integrity verification:** Recalculate hashes and check
    previous-hash links.
-   **Digital certificate:** View or print a simple certificate for a
    record.
-   **JSON persistence:** Save the chain in `blockchain.json` so it can
    be loaded after restart.
-   **Web interface:** Use browser pages for the application's main
    functions.

Feature availability depends on the exact project version being run.

## Technology Stack

  Technology            Purpose
  --------------------- -----------------------------------------
  Python                Application and blockchain logic
  Flask                 Web server and routes
  HTML5                 Page structure and forms
  CSS                   Styling and layout
  JavaScript            Frontend interactions where implemented
  SHA-256 (`hashlib`)   Block hashing and integrity checks
  JSON                  Local data persistence
  Jinja2                Rendering HTML templates

## How It Works

1.  A user opens the web application.
2.  The user submits a registration or ownership-transfer form.
3.  Flask receives the request and processes the form data.
4.  Python creates a block for the transaction.
5.  The block stores an index, timestamp, land data, previous hash, and
    calculated hash.
6.  The chain is saved to `blockchain.json`.
7.  The verification feature recalculates hashes and checks block links.

``` text
Register Land / Transfer Ownership
                 |
                 v
          Flask Application
                 |
                 v
        Python Blockchain Logic
                 |
                 v
             Create Block
                 |
                 v
             SHA-256 Hash
                 |
                 v
       Link Previous Block Hash
                 |
                 v
        Save to blockchain.json
                 |
                 v
        Verify Chain Integrity
```

## Architecture

-   **Presentation:** HTML templates, CSS, and JavaScript.
-   **Application:** Flask routes and form handling.
-   **Blockchain:** Python code for blocks, hashing, linking, and
    verification.
-   **Storage:** A local `blockchain.json` file.

**Important:** This is a custom Python blockchain prototype. JSON
persistence is not a distributed blockchain network. The current version
has no distributed consensus, Ethereum deployment, or smart-contract
execution.

## Project Structure

``` text
LandChain/
├── app.py
├── blockchain.py
├── blockchain.json
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── register_land.html
│   ├── transfer_land.html
│   ├── verify_land.html
│   ├── blockchain.html
│   ├── land_details.html
│   └── certificate.html
└── static/
    ├── style.css
    └── script.js
```

Your folder may differ slightly by version. Ensure template filenames
match the names referenced by `app.py`.

## Requirements

-   Python 3
-   `pip`
-   A modern web browser
-   Git (optional, for GitHub)

## Installation

### 1. Clone the repository

``` bash
git clone https://github.com/bhavyweb3/LandChain-LandRegistrySystem.git
cd LandChain-Blockchain-Land-Registry
```

If the project is not on GitHub yet, open your local project folder
instead.

### 2. Create and activate a virtual environment (Windows PowerShell)

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is missing, `Flask` may be installed as a
temporary fallback:

``` powershell
python -m pip install Flask
```

Keep `requirements.txt` updated for reproducible installation.

## Run the Application

From the project folder:

``` powershell
python app.py
```

Open the local address shown in the terminal. With the usual Flask
development configuration, it is:

``` text
http://127.0.0.1:5000/
```

Stop the server with `Ctrl + C`. The Flask development server is for
local testing, not production hosting.

## Using LandChain

1.  Start the Flask app and open its local URL.
2.  Sign in if the current version requires login. Confirm any demo
    credentials from the source code before publishing them.
3.  Use the dashboard to review available summaries.
4.  Use **Register Land** to add fictional sample data.
5.  Open the record details or verification page.
6.  Use **Transfer Land** to record a sample transfer.
7.  Open **Blockchain** to inspect blocks and hashes.
8.  Run integrity verification.
9.  Open the certificate page to view or print a sample certificate.

Use fictional data in public demonstrations. Do not enter sensitive
personal or real property information.

## Blockchain Design

### Block fields

  Field             Meaning
  ----------------- ---------------------------------------------
  `index`           Position of the block in the chain
  `timestamp`       Time the block was created
  `land_data`       Registration or transfer data
  `previous_hash`   Hash stored by the previous block
  `hash`            SHA-256 hash calculated from block contents

### Genesis block

The genesis block is the first block (index `0`). In this
implementation, its previous-hash value is `"0"`.

### SHA-256 hashing

Python's `hashlib.sha256()` creates a fixed-length hexadecimal digest
from block data. Changing the input normally changes the resulting hash.
The verification feature compares a stored hash with a recalculated
hash.

### Previous-hash linking

Each block after the genesis block stores the previous block's hash.
Verification checks whether that value matches the preceding block's
actual hash.

### Ownership history

A transfer is recorded as a new event rather than erasing the earlier
transaction. The application can use these events to display transaction
history.

### What hashing does not prove

Hash checks can detect inconsistencies, but they do not prove that
submitted information is true or that a person legally owns a property.
Since this version stores data in a local JSON file, someone with
sufficient access could modify the file and recompute the chain. There
is no distributed consensus in this version.

## Limitations and Security

-   Educational prototype, not a production land registry.
-   Local JSON storage is not distributed blockchain storage.
-   No Solidity, MetaMask, Ethereum, or public testnet integration in
    this version.
-   Hard-coded demo authentication, if present, is not suitable for
    production.
-   Never commit passwords, private keys, API secrets, or sensitive
    personal information.
-   A generated certificate is a demo document, not legal proof of
    ownership.
-   The project has not been represented as audited or production-ready.

## Testing

Suggested classroom checks: 1. Register a unique sample land ID and
confirm it appears. 2. Restart the app and check that the record
persists. 3. Transfer a sample record and confirm the earlier
transaction remains. 4. Inspect the `previous_hash` values in the
blockchain explorer. 5. Run integrity verification on an unchanged
chain. 6. In a disposable test copy only, change a block's data in
`blockchain.json` without updating its hash and rerun verification. Back
up the file first.

## Future Scope

-   Add a Solidity `LandRegistry` smart contract.
-   Connect MetaMask through Ethers.js.
-   Test on a local Ethereum development network before a public
    testnet.
-   Add secure authentication and role-based access.
-   Add automated tests and stronger input validation.
-   Display transaction identifiers and richer ownership history.
-   Store large documents off-chain and record their hashes on-chain.
-   Add QR codes for certificate lookup.
-   Improve accessibility and mobile responsiveness.
-   Explore document verification and carefully designed anomaly alerts.

These are future improvements, not current features unless separately
implemented.

## Contributing

1.  Fork the repository.
2.  Create a branch for your change.
3.  Make a focused change and test it locally.
4.  Commit with a clear message.
5.  Open a pull request describing the change.

Do not submit real property records, credentials, private keys, or
confidential information.

## Disclaimer

LandChain is developed for educational and demonstration purposes. It is
not affiliated with a government land-record authority and does not
replace official property records, title verification, registration
procedures, or legal advice. Use fictional demo data.

## Author and Acknowledgements

-   **Project:** LandChain --- Blockchain-Based Land Registry System
-   **Type:** Academic / student prototype
-   **Developer:** Add your name and team details here if you want them
    shown publicly.

Thanks to the educators, documentation authors, and open-source
communities whose resources support learning in Python, Flask,
cryptography, and blockchain development.

## License

No license has been specified. If you want others to reuse, modify, or
distribute the project, choose a license (for example, MIT) and add a
`LICENSE` file. Do not claim a license until that file is included.
