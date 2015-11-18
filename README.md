# Arris_Harvest
Harvest Arris firmware

#### enumerate files
http://arris.force.com/consumers/ConsumerProductDetail?p=a0ha000000NJnxXAAT&c=Touchstone%20Modems%20and%20Gateways#panel4 
>>> $('div#panel4 div.medium-4 div.small-9 div')[0].textContent.trim()
  "USB Drivers Win 98 SE"

#### click tab 'Firmware'
>>> $('dl.small-12 a')[3].textContent.trim()
 "Drivers & Firmware"

#### get Model Name
>>> $('div.medium-6:nth-child(2) div:nth-child(1)  p')[0].textContent.trim()
 "CM550"
>>> var modelDesc = $('div.medium-6:nth-child(2) > div:nth-child(3) > p:nth-child(1)')[0].textContent.trim()
