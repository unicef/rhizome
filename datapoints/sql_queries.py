
## this should show in red if the COUNT is less than the total
## number of regions that exist for that relationshiop

show_dashboard = '''
        SELECT
             i.indicator_pct_display_name
            , d.value / d2.value as pct
            , r.full_name
        FROM datapoint d
        INNER JOIN indicator_pct i
            ON d.indicator_id = i.indicator_part_id
        INNER JOIN datapoint d2
            ON i.indicator_whole_id = d2.indicator_id
            AND d.reporting_period_id = d2.reporting_period_id
            AND d.region_id = d2.region_id
        INNER JOIN region r
            ON d.region_id = r.id

        UNION ALL

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
        GROUP BY r.full_name, i.name,i.id ,d.reporting_period_id
        '''
