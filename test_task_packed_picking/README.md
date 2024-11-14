# Test Task Packed Picking

**Version**: 16.0.1.0.0 **Category**: Inventory **Summary**: A custom Odoo module
designed to enhance stock picking operations by adding advanced packing and validation
features.

**View module demo (YouTube Video):**
[![View module demo](http://img.youtube.com/vi/3g4oYoNwFnw/0.jpg)](https://youtu.be/3g4oYoNwFnw)

## Overview

The **Test Task Packed Picking** module extends Odoo's standard stock picking
functionality, introducing custom methods for creating and managing product packages.
With this module, users can create `stock.picking` records that pack selected products
into customizable packages, handle serial numbers, create product lots, and validate the
picking process.

This module is particularly useful for warehouses and inventory operations that require
precise packing, tracking, and inventory validation workflows.

## Key Features

- **Custom Packing Functionality**: Automatically pack selected products into specified
  packages.
- **Advanced Stock Picking Management**: Enables setting quantities, creating lots, and
  validating pickings.
- **Wizard Interface**: Provides a wizard to simplify and automate the packed picking
  creation process.
- **User Notifications**: Notifies assigned users about new packed pickings.

## Directory Structure

```plaintext
.
├── __init__.py                                 # Initialize the module
├── __manifest__.py                             # Module metadata and dependencies
├── models/                                     # Business logic and custom model extensions
│   ├── __init__.py                             # Initialize models
│   ├── packed_picking_stock_picking.py         # Extends stock.picking model with packing logic
│   └── __pycache__/                            # Compiled Python files (auto-generated)
├── security/                                   # Access control and security settings
│   └── ir.model.access.csv                     # Defines user permissions for the module
├── tests/                                      # Unit tests for the module
│   ├── __init__.py                             # Initialize tests
│   ├── test_stock_picking_packed_picking.py    # Tests for stock picking features
│   └── __pycache__/                            # Compiled test files (auto-generated)
└── wizards/                                    # Wizard logic and views
    ├── __init__.py                             # Initialize wizards
    ├── packed_picking_wizard.py                # Wizard model for packed picking creation
    ├── packed_picking_wizard_views.xml         # XML views for the wizard
    └── __pycache__/                            # Compiled wizard files (auto-generated)
```

## Installation

1. Clone the repository into your custom addons directory:

   ```bash
   git clone https://github.com/tendil/test_task_packed_picking.git
   ```

2. Restart your Odoo server to recognize the new module:

   ```bash
   ./odoo-bin -c /path/to/your/config.conf -d your_database
   ```

3. Activate the developer mode in Odoo, navigate to **Apps**, and update the app list.
4. Search for "Test Task Packed Picking" and install the module.

## Configuration

1. Go to **Inventory > Configuration > Warehouse Management > Operations Types** and
   configure your picking types as required.
2. Set up any user permissions through **Settings > Users & Companies > Users** if
   needed (based on `ir.model.access.csv`).

## Usage

1. **Creating a Packed Picking**:

   - Go to **Inventory > Operations > Pack Products** to open the wizard interface.
   - Select the desired `Operation Type`, `Source` and `Destination Locations`, specify
     the `Package Name`, and optionally choose to create lots or validate the picking
     immediately.
   - Add product lines with their respective quantities and serial numbers if required.
   - Click **Create Picking** to generate the packed picking.

2. **Validating and Tracking**:
   - The module automatically sets up packages with the specified configurations and
     updates the stock picking status as needed.
   - Notifications are sent to the responsible user if configured.

## Development and Testing

### Running Tests

The module includes unit tests to ensure its reliability and correct functionality. To
run the tests:

1. Install the module in a testing environment.
2. Execute the following command:

   ```bash
   ./odoo-bin -c /path/to/your/config.conf -u test_task_packed_picking --test-enable --stop-after-init
   ```

This command will install the module, run all available tests in the `tests` folder, and
stop the server after completing the tests.

### Test Coverage

- **Basic Picking Creation**: Ensures that a picking record can be created with the
  specified products and quantities.
- **Packing and Validation**: Tests that products are packed correctly and that picking
  can be set to "Ready" if required.
- **Wizard Automation**: Verifies that the wizard successfully gathers user inputs and
  creates the picking with proper notification.

## Contributing

Contributions are welcome! If you have improvements, please fork the repository, create
a branch, and submit a pull request. For significant changes, please open an issue first
to discuss the proposed changes.

## License

This module is licensed under the **AGPL-3 License**. See the LICENSE file for more
details.

## Support

- [Telegram](https://t.me/XllrepoDevelloper)
