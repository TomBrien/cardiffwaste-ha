# Cardiff Waste: Home Assistant Integration

A, currently very, basic integration to provide waste collection date sensors for those whose waste is collected by Cardiff Council.

## Please Note

Right now this integration is in early-stage development still. It works for me and contains some basic address validation so should be robust but right now anyone else's mileage may vary.

## Installation

### HACS

1. Add this repository as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories) in HACS
2. Search for and download the "Cardiff Waste" integration
3. Restart your Home Assistant

### Manual 

1. Copy the `cardiffwaste` folder from this repository to the `custom_components` repository in your Home Assistant's configuration directory (the same place as your `configuration.yaml`)
2. Restart you Home Assistant

## Configuration

For ease you can skip the first two steps using this my.home-assistant link:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=cardiffwaste)

1. Go to Devices & Services in Configuration
2. Click Add Intrgeation and select Cardiff Waste
3. When prompted, enter the unique property reference number (UPRN) of your property. You can find this using [this site](https://www.findmyaddress.co.uk/search)
