export default [

  {
    'id': 1,
    'title': 'Management Dashboard: National Indicators',
    'location_level': 1,
    'indicators': [
      { 'type': 'section-header', 'title': 'Resources' },
      { 'id': 44 },
      { 'id': 43 },
      { 'id': 32 },
      { 'id': 31 }
    ]
  },

  {
    'id': 3,
    'title': 'Management Dashboard: Provincial Indicators',
    'location_level': 1,
    'indicators': [

      { 'type': 'section-header', 'title': 'Immunity Gap' },
      { 'id': 431, 'name': 'Non-polio AFP cases with zero doses of OPV' },
      { 'id': 432, 'name': 'Non-polio AFP cases with 1-3 doses of OPV' },
      { 'id': 433, 'name': 'Non-polio AFP cases with 4+ doses of OPV' },

      { 'type': 'section-header', 'title': 'Polio+' },
      { 'id': 29, 'name': 'Number of caregivers in high risk districts' },
      { 'id': 50, 'name': 'Number of caregivers in HRD who know times needed to visit RI site before 1 yo' }

    ]
  },

  {
    'id': 2,
    'title': 'Management Dashboard: District Indicators',
    'location_level': 4,
    'indicators': [

      { 'type': 'section-header', 'title': 'District Info' },
      { 'id': 195, 'name': 'Is a high risk district? (1=yes, 0=no)' },
      { 'id': 55, 'name': 'Number of children targeted in high-risk districts' },

      { 'type': 'section-header', 'title': 'Polio Cases' },
      { 'id': 70, 'name': 'Number of WPV1 cases' },
      { 'id': 160, 'name': 'Number of WPV3 cases' },
      { 'id': 69, 'name': 'Number of cVDPV2 cases' },

      { 'type': 'section-header', 'title': 'Supply' },
      { 'id': 5, 'name': 'Number of vaccine doses used in HRD' },
      { 'id': 51, 'name': 'Number of children vaccinated in HRD' },
      { 'id': 196, 'name': 'HR district did NOT receive polio vaccine supply at least 3 days before the planned start date of campaign (1 = yes, 0 = no)' },
      { 'id': 197, 'name': 'District reported on balance of SIA vaccine stocks after last SIA round? (1=yes, 0=no)' },
      { 'id': 198, 'name': 'Number of functional active cold chain equipment in the district' },
      { 'id': 199, 'name': 'Total number of all active cold chain equipment in district' },
      { 'id': 472, 'name': 'Is a high risk district where at least 90% of active cold chain equipment are functional (1=yes, 0=no)' },
      { 'id': 221, 'name': 'Is an HRD that has polio vaccine wastage rate in SIAs between 5 and 15% (1=yes, 0=no)' },

      { 'type': 'section-header', 'title': 'Access' },
      { 'id': 158, 'name': 'Number of children missed due to all access issues' },
      { 'id': 175, 'name': 'Number of established LT vaccination transit points' },
      { 'id': 176, 'name': 'Number of established LT vaccination transit points with a dedicated social mobilizer' },
      { 'id': 177, 'name': 'Number of children vaccinated at transit points last month' },
      { 'id': 203, 'name': 'Is an access-challenged district (1=yes, 0=no)' },
      { 'id': 202, 'name': 'Is an access-challenged district that has a specific access approach identified (1=yes, 0=no)' },
      { 'id': 204, 'name': 'Total number of LT vaccination transit points planned by the programme' },
      { 'id': 434, 'name': 'Reason for inaccessible children - Perception of fear' },
      { 'id': 435, 'name': 'Reason for inaccessible children - Local community not supportive' },
      { 'id': 436, 'name': 'Reason for inaccessible children - Crime' },
      { 'id': 437, 'name': 'Reason for inaccessible children - Militant / Anti-Govt Elements' },
      { 'id': 438, 'name': 'Reason for inaccessible children - Security Operations / Incidents' },
      { 'id': 439, 'name': 'Reason for inaccessible children - Management issues' },
      { 'id': 440, 'name': 'Reason for inaccessible children - Environment issues' },
      { 'id': 441, 'name': 'Reason for inaccessible children - Political issues' },
      { 'id': 451, 'name': 'Reason for inaccessible children - No reason provided' },

      { 'type': 'section-header', 'title': 'Frontline Workers\' Capacity To Perform' },
      { 'id': 205, 'name': 'HR sub-district has at least 1 permanent SM (1=yes, 0=no)' },
      { 'id': 207, 'name': 'Target number of social mobilizers and supervisors' },
      { 'id': 41, 'name': 'Number of vaccinators and social mobilizers' },
      { 'id': 206, 'name': 'Number of social mobilizers and supervisors in place' },
      { 'id': 36, 'name': 'Number of social mobilizers in place' },
      { 'id': 40, 'name': 'Number of female social mobilizers' },
      { 'id': 209, 'name': 'Number of social mobilizers trained or refreshed with the integrated health package in the last 6 months' },
      { 'id': 210, 'name': 'Number of social mobilizers who received on-the-job supervision during their last working week' },
      { 'id': 463, 'name': 'number of social mobilisers participating the telephone survey' },
      { 'id': 46, 'name': 'Number of social mobilizers receiving timely payment for last campaign' },
      { 'id': 33, 'name': 'Number of high risk sub-districts' },
      { 'id': 34, 'name': 'Number of high risk sub-districts covered by at least 1 social mobilizer' },
      { 'id': 38, 'name': 'Number of vaccination teams' },
      { 'id': 37, 'name': 'Number of vaccination teams with at least one female' },
      { 'id': 208, 'name': 'Number of vaccination teams with at least 1 member from the local community' },
      { 'id': 42, 'name': 'Number of vaccinators and SMs operating in HRDs trained on professional IPC package in last 6 months' },

      { 'type': 'section-header', 'title': 'Performance of FLWs' },
      { 'id': 213, 'name': 'Number of absences before re-visit' },
      { 'id': 214, 'name': 'Number of absences after re-visit' },
      { 'id': 222, 'name': 'Number of microplans with minimum social data out of 10 randomly selected microplans from previous campaign in selected HR areas' },
      { 'id': 25, 'name': 'Number of refusals before re-visit' },
      { 'id': 26, 'name': 'Number of refusals after re-visit' },

      { 'type': 'section-header', 'title': 'Missed Children' },
      { 'id': 264, 'name': 'Number of children missed due to refusal' },
      { 'id': 251, 'name': 'Number of children missed due to child not available' },
      { 'id': 268, 'name': 'Number of children missed due to no team/team did not visit' },
      { 'id': 24, 'name': 'Number of children missed due to other reasons' },

      { 'type': 'section-header', 'title': 'Polio+' },
      { 'id': 218, 'name': 'Number of high risk districts with locations where OPV is delivered together with any other polio-funded services demanded by community' },
      { 'id': 243, 'name': 'Number of children 12 months and under' },
      { 'id': 244, 'name': 'Number of children under 12 months who received DPT3 or Penta3' },
      { 'id': 217, 'name': 'Number of RI sessions monitored' },
      { 'id': 216, 'name': 'Number of RI sessions monitored having stockouts of any vaccine in the last month' },
      { 'id': 192, 'name': 'Number of RI defaulters mobilized by SMs last month' },
      { 'id': 473, 'name': 'District was sampled for microplan review  (1=yes, 0=no)' },
      { 'id': 474, 'name': 'District passed microplan review (1=yes, 0=no)' }

    ]
  }

]
