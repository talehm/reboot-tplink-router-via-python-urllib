# reboot-tplink-router-via-python-urllib
Rebooting Tp-link WR840N v2 via URLLIB

You can reboot your tp-link router via python urllib package.

## Prerequesties:
* python v3
* Access to the router
## Tested Models
<table>
    <tr>
    <th>Hardware Version</th>
    <th>Firmware Version</th>
    </tr>
<tr>
<td>
WR840N v2
</td>
<td>
3.16.9 Build 160406 Rel.40792n 
</td>
</tr>

    <tr>
<td>
WR841N v12
</td>
<td>
3.16.9 Build 160624 Rel.44986n </td>
</tr>
</table>

## Example

```python 
    message, status = runScript( Router_Name, ip_address, username, password )
    if status:
       print("`{} : REBOOTED BY URLLIB ".format(Router_Name))
    elif message == 403:
       print(" NOT REBOOTED BY URLLIB > 403 Forbidden ")
    else:
       print("`{} : NOT REBOOTED BY URLLIB > Error: {} ".format( Router_Name, message)) 
 ```
