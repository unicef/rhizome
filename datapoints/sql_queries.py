
## this should show in red if the COUNT is less than the total
## number of regions that exist for that relationshiop


show_region_aggregation = '''
        SELECT
            i.name
            , SUM(d.value) as value
            , r.full_name
        FROM region_relationship rr
        INNER JOIN datapoint d
            ON rr.region_1_id = d.region_id
        INNER JOIN indicator i
            ON d.indicator_id = i.id
        INNER JOIN region r
            ON rr.region_0_id = r.id
        GROUP BY r.full_name, i.name,i.id ,d.campaign_id
        '''
