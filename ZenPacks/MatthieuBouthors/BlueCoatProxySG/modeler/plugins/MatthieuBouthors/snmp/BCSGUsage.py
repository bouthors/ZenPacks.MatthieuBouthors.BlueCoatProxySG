from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class BCSGUsage(SnmpPlugin):
    relname = 'blueCoatSGUsages'
    modname = 'ZenPacks.MatthieuBouthors.BlueCoatProxySG.BlueCoatSGUsage'


    snmpGetTableMaps = (
        GetTableMap(
            'tempUsageTable', '.1.3.6.1.4.1.3417.2.4.1.1.1', {
                '.3': 'deviceUsageName',
                }
            ),
        )

    def process(self, device, results, log):
        temp_Usage = results[1].get('tempUsageTable', {})
	log.info(temp_Usage)

	rm = self.relMap()
        for snmpindex, row in temp_Usage.items():
            name = row.get('deviceUsageName')
            if not name:
                log.warn('Skipping usage with no name')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
                'deviceUsageName': name,
                'snmpindex': snmpindex.strip('.'),
                }))
	log.info(rm)

        return rm

