<?php
$this->db->query("INSERT INTO `" . DB_PREFIX . "order_fraud` SET order_id = '" . (int)$order_id . "', customer_id = '" . (int)$customer_id . "', country_match = '" . $this->db->escape($country_match) . "', country_code = '" . $this->db->escape($country_code) . "', high_risk_country = '" . $this->db->escape($high_risk_country) . "', distance = '" . (int)$distance . "', ip_region = '" . $this->db->escape($ip_region) . "', ip_city = '" . $this->db->escape($ip_city) . "', ip_latitude = '" . $this->db->escape($ip_latitude) . "', ip_longitude = '" . $this->db->escape($ip_longitude) . "', ip_isp = '" . $this->db->escape($ip_isp) . "', ip_org = '" . $this->db->escape($ip_org) . "', ip_asnum = '" . (int)$ip_asnum . "', ip_user_type = '" . $this->db->escape($ip_user_type) . "', ip_country_confidence = '" . $this->db->escape($ip_country_confidence) . "', ip_region_confidence = '" . $this->db->escape($ip_region_confidence) . "', ip_city_confidence = '" . $this->db->escape($ip_city_confidence) . "', ip_postal_confidence = '" . $this->db->escape($ip_postal_confidence) . "', ip_postal_code = '" . $this->db->escape($ip_postal_code) . "', ip_accuracy_radius = '" . (int)$ip_accuracy_radius . "', ip_net_speed_cell = '" . $this->db->escape($ip_net_speed_cell) . "', ip_metro_code = '" . (int)$ip_metro_code . "', ip_area_code = '" . (int)$ip_area_code . "', ip_time_zone = '" . $this->db->escape($ip_time_zone) . "', ip_region_name = '" . $this->db->escape($ip_region_name) . "', ip_domain = '" . $this->db->escape($ip_domain) . "', ip_country_name = '" . $this->db->escape($ip_country_name) . "', ip_continent_code = '" . $this->db->escape($ip_continent_code) . "', ip_corporate_proxy = '" . $this->db->escape($ip_corporate_proxy) . "', anonymous_proxy = '" . $this->db->escape($anonymous_proxy) . "', proxy_score = '" . (float)$proxy_score . "', is_trans_proxy = '" . $this->db->escape($is_trans_proxy) . "', free_mail = '" . $this->db->escape($free_mail) . "', carder_email = '" . $this->db->escape($carder_email) . "', high_risk_username = '" . $this->db->escape($high_risk_username) . "', high_risk_password = '" . $this->db->escape($high_risk_password) . "', bin_match = '" . $this->db->escape($bin_match) . "', bin_country = '" . $this->db->escape($bin_country) . "',  bin_name_match = '" . $this->db->escape($bin_name_match) . "', bin_name = '" . $this->db->escape($bin_name) . "', bin_phone_match = '" . $this->db->escape($bin_phone_match) . "', bin_phone = '" . $this->db->escape($bin_phone) . "', customer_phone_in_billing_location = '" . $this->db->escape($customer_phone_in_billing_location) . "', ship_forward = '" . $this->db->escape($ship_forward) . "', city_postal_match = '" . $this->db->escape($city_postal_match) . "', ship_city_postal_match = '" . $this->db->escape($ship_city_postal_match) . "', score = '" . (float)$score . "', explanation = '" . $this->db->escape($explanation) . "', risk_score = '" . (float)$risk_score . "', queries_remaining = '" . (int)$queries_remaining . "', maxmind_id = '" . $this->db->escape($maxmind_id) . "', error = '" . $this->db->escape($error) . "', date_added = NOW()");
?>