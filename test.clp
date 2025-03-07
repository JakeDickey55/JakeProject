(deftemplate market-data
  (slot total_mcap)
  (slot btc_dominance)
  (slot eth_dominance)
  (slot coins_count)
  (slot active_markets)
  (slot total_volume)
  (slot mcap_change)
  (slot volume_change)
  (slot avg_change_percent))

(defrule btc-dominance-high
  (market-data (btc_dominance ?btc_dominance&:(> ?btc_dominance 50)))
  =>
  (printout t "BOOM" crlf))


