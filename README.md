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

Python
```python
In [444]: driver.current_url
Out[444]: 'http://arris.force.com/consumers/ConsumerProductDetail?p=a0ha000000GNcscAAD&c=SURFboard%20Modems%20and%20Gateways'

In [445]: CSS = driver.find_element_by_css_selector

In [446]: CSS('div.medium-6:nth-child(2) div  p').text
Out[446]: 'SB6121'

In [447]: CSS('div.medium-6:nth-child(2) div:nth-child(3) p').text
Out[447]: 'The SB6121 delivers your complete personal media experience, at incredible broadband speeds. It harnesses the power of DOCSIS 3.0 technology to bond up to four downstream channels and four upstream channels— providing you advanced multimedia services with download speeds up to 172 Mbps in each direction. That makes surfing, shopping, and downloading far more realistic, faster, and efficient than ever before.'

In [448]: CSS('div.medium-6 > div:nth-child(2) > p').text
Out[448]: 'SURFboard® Cable Modem'

In [454]: str([_.text for _ in CSSs('dl.small-12 a')])
Out[454]: "['FAQs', 'Specifications', 'Manuals & Documentation', 'Drivers & Firmware', 'Related Product Videos']"

In [465]: CSS('#tab4 > a:nth-child(1)').click()

In [466]: CSS('h5.text-center').text
Out[466]: 'No Drivers & Firmware Currently Available'
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

```python
In [435]: driver.current_url
Out[435]: 'http://arris.force.com/consumers/ConsumerProductlist?c=SURFboard%20Modems%20and%20Gateways'

In [434]: str([_.text for _ in CSSs('div.medium-9 div.prodContainer') if _.is_displayed()])
Out[434]: "['SB6121', 'SB6141', 'SB6182', 'SB6183', 'SB6190', 'SBG6400', 'SBG6580', 'SBG6700-AC', 'SBG6782-AC', 'SBG6900-AC', 'SBR-AC1750']"
In [441]: len([_ for _ in CSSs('div.medium-9 div.small-12') ])
Out[441]: 11

In [442]: [_ for _ in CSSs('div.medium-9 div.small-12') ]
Out[442]: 
[<selenium.webdriver.remote.webelement.WebElement (session="ab170950-bda1-4b37-97c2-330c8ab98349", element="{cbe0fec0-a261-4e94-9d82-8e3c36c58ff6}")>,
... ] # 11 == len(WebElement)

In [443]: _442[0].click()

In [444]: driver.current_url
Out[444]: 'http://arris.force.com/consumers/ConsumerProductDetail?p=a0ha000000GNcscAAD&c=SURFboard%20Modems%20and%20Gateways'
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
