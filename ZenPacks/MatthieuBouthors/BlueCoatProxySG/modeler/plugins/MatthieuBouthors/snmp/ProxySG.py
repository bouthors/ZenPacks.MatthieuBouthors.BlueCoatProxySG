from Products.DataCollector.plugins.CollectorPlugin import (
    SnmpPlugin, GetTableMap,
    )


class ProxySG(SnmpPlugin):
    relname = 'blueCoatSGHealthChecks'
    modname = 'ZenPacks.MatthieuBouthors.BlueCoatProxySG.BlueCoatSGHealthCheck'


    snmpGetTableMaps = (
        GetTableMap(
            'tempHealthCheckTable', '.1.3.6.1.4.1.3417.2.7.1.2.1.1', {
                '.1': 'DeviceHealthCheckName',
                }
            ),
        GetTableMap(
            'tempUsageTable', '.1.3.6.1.4.1.3417.2.4.1.1.1', {
                '.3': 'deviceUsageName',
                }
            ),
        GetTableMap(
            'tempDiskTable', '.1.3.6.1.4.1.3417.2.2.1.1.1.1', {
                '.5': 'deviceDiskVendor',
                '.6': 'deviceDiskProduct',
                '.7': 'deviceDiskRevision',
                '.8': 'deviceDiskSerialN',
                '.9': 'deviceDiskBlockSize',
                '.10': 'deviceDiskBlockCount',
                }
            ),
        )

    def process(self, device, results, log):
        temp_HC = results[1].get('tempHealthCheckTable', {})
        temp_Usage = results[1].get('tempUsageTable', {})
        temp_Disk = results[1].get('tempDiskTable', {})
	log.info(temp_HC)
	log.info(temp_Usage)
	log.info(temp_Disk)

	rm = self.relMap()
        for snmpindex, row in temp_HC.items():
            name = row.get('DeviceHealthCheckName')
            if not name:
                log.warn('Skipping health check with no name')
                continue

            rm.append(self.objectMap({
                'id': self.prepId(name),
                'deviceHealthCheckName': name,
                'snmpindex': snmpindex.strip('.'),
                }))
	log.info(rm)

        relname = 'blueCoatSGUsage'
        modname = 'ZenPacks.MatthieuBouthors.BlueCoatProxySG.BlueCoatSGUsage'

	rm2 = self.relMap()
        for snmpindex, row in temp_Usage.items():
            name = row.get('deviceUsageName')
            if not name:
                log.warn('Skipping usage with no name')
                continue

            rm2.append(self.objectMap({
                'id': self.prepId(name),
                'deviceUsageName': name,
                'snmpindex': snmpindex.strip('.'),
                }))
	log.info(rm2)

#        log(rm)
        return rm

