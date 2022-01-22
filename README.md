# Cardiff Waste: Home Assistant Integration

A, currently very, basic integration to provide waste collection date sensors for those whose waste is collected by Cardiff Council.

## Installation

### HACS

1. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) in HACS
2. Search for and download the "Cardiff Waste" integration
3. Restart your Home Assistant
4. Follow the [setup](#setup) instructions below

### Manual 

1. Copy the `cardiffwaste` folder from this repository to the `custom_components` repository in your Home Assistant's configuration directory (the same place as your `configuration.yaml`)
2. Restart you Home Assistant
3. Follow the [setup](#setup) instructions below

### Setup

For ease you can skip the first two steps using this my.home-assistant link:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=cardiffwaste)

1. Go to Devices & Services in Configuration
2. Click Add Integration and select Cardiff Waste
3. When prompted, enter the unique property reference number (UPRN) of your property. You can find this using [this site](https://www.findmyaddress.co.uk/search)

### Configuration

By default, sensors will be created for the next food waste, garden waste, general waste and recycling collections. You can removed or reenable any of these by clicking on the "Configure" button in the Cardiff Waste panel within Devices & Services form the Configuration menu.

