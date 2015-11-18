# Arris_Harvest
Harvest Arris firmware

### Model Detail Page 
http://arris.force.com/consumers/ConsumerProductDetail?p=a0ha000000NJnxXAAT&c=Touchstone%20Modems%20and%20Gateways#panel4 

#### enumerate files
```javascript
$('div#panel4 div.medium-4 div.small-9 div')[0].textContent.trim();
"USB Drivers Win 98 SE"
```

#### click tab 'Firmware'
```javascript
$('dl.small-12 a')[3].textContent.trim();
"Drivers & Firmware"
```

#### get Model Name
```javascript
$('div.medium-6:nth-child(2) div:nth-child(1)  p')[0].textContent.trim();
"CM550"
var modelDesc = $('div.medium-6:nth-child(2) > div:nth-child(3) > p:nth-child(1)')[0].textContent.trim();
```

#### get Model Picture
```javascript
var aa= $('.box.boxProduct')[0];
aa.getAttribute('style');
"background: url(https://arris--c.na13.content.force.com/servlet/servlet.ImageServer?id=015a0000003NYHt&oid=00D30000000kUAL&lastMod=1442430676000);"
```

### enumerate models under Touchstone series
http://arris.force.com/consumers/ConsumerProductList?c=Touchstone%20Modems%20and%20Gateways

#### get all button links to Model Detail Page
```javascript
$('div.large-4  a.button');
```

#### get all model names
```javascript
$('div.large-4  h6')[87].textContent.trim();
"WTM652G/NA"
```
 
#### get picture of model
```javascript
var aa = $('div.box.boxProduct')[0];
aa.getAttribute('style');
"background: url(https://arris--c.na13.content.force.com/servlet/servlet.ImageServer?id=015a0000003NYHt&oid=00D30000000kUAL&lastMod=1442430676000);"
```

### enumerate series under Arris Support Home
http://arris.force.com/consumers

```python
In [379]: driver = harvest_utils.getFirefox()
In [381]: driver.get('http://arris.force.com/consumers')

In [384]: len(CSSs('div.small-12 a.button'))
Out[384]: 8

In [385]: str([_.text for _ in CSSs('div.small-12 h6')])                                  
Out[385]: "['SURFboard® CABLE MODEMS AND GATEWAYS', 'TOUCHSTONE CABLE MODEMS AND GATEWAYS', 'CABLE SET-TOP BOX', 'DSL MODEMS AND GATEWAYS', 'NETWORK ADAPTERS', 'DISCONTINUED PRODUCTS', 'REMOTE ACCESS SOFTWARE', 'ARRIS FOLLOW ME TV™\\nMOBILE APPLICATION HELP']"

In [387]: str([_.get_attribute('href') for _ in CSSs('div.small-12 a.button')])
Out[387]: "['http://arris.force.com/consumers/ConsumerProductlist?c=SURFboard%20Modems%20and%20Gateways', 'http://arris.force.com/consumers/ConsumerProductlist?c=Touchstone%20Modems%20and%20Gateways', 'http://arris.force.com/consumers/ConsumerProductlist?c=Cable%20Set-Top%20Box', 'http://arris.force.com/consumers/ConsumerProductlist?c=DSL%20Modems%20and%20Gateways', 'http://arris.force.com/consumers/ConsumerProductlist?c=Network%20Adapters', 'http://arris.force.com/consumers/ConsumerProductlist?c=Discontinued', 'http://arris.force.com/consumers/ConsumerProductlist?c=Remote%20Access%20Software', 'http://arris.force.com/consumers/ConsumerMobileAppHelp']"
```
