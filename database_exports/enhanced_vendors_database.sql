-- Enhanced Vendor Database SQL Import Script
-- Generated on: 2025-10-24 10:24:37


-- Create enhanced tables
CREATE TABLE IF NOT EXISTS vendors (
    vendor_id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    domain VARCHAR(255),
    description TEXT,
    title VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(255),
    total_pages_scraped INT DEFAULT 0,
    scraped_at DATETIME,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    url VARCHAR(255),
    pricing VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    url VARCHAR(255),
    pricing VARCHAR(100),
    target_audience TEXT,
    requirements TEXT,
    deployment TEXT,
    support TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS service_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    service_name VARCHAR(255),
    use_case TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS product_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    product_name VARCHAR(255),
    use_case TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS technology_stack (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    technology VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS industries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    industry VARCHAR(100),
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS general_features (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    feature TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS general_benefits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    benefit TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS general_use_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    use_case TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS integrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    integration TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

CREATE TABLE IF NOT EXISTS certifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_id VARCHAR(50),
    certification TEXT,
    FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
);

-- Insert vendor data

-- Insert vendor: Arctic Wolf | We Make Security Work
INSERT INTO vendors (vendor_id, company_name, website, domain, description, title, contact_email, contact_phone, total_pages_scraped, scraped_at, last_updated) VALUES (
    'arctic_wolf_we_make_security_work',
    'Arctic Wolf | We Make Security Work',
    'https://arcticwolf.com',
    'arcticwolf.com',
    'Arctic Wolf delivers dynamic, 24x7 AI-driven cybersecurity protection tailored to the needs of your organization. Ready to boost your cyber resilience?',
    'Arctic Wolf | We Make Security Work',
    'pr@arcticwolf.com',
    '3202806040',
    86,
    '2025-10-24T10:11:08.435701',
    '2025-10-24T10:22:10.432016'
);

INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'security', 'G', 'https://arcticwolf.com/solutions/industries/government/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsSchool DistrictsHigher EducationCities & CountiesLocal GovernmentState AgenciesHealthcare OrganizationsReligious OrganizationsNon');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsTexas State AgenciesCountiesLocal GovernmentPublic Education(Out of State with ICC Agreements)Higher EducationCommunity CollegesK');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsState GovernmentsLocal GovernmentsHigher EducationK');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', '12 EducationNon');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'in attacks to government and civic organizations in 2024 over the prior year');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'productivity at a lower cost');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'security', 'r', 'https://arcticwolf.com/solutions/endpoint-security/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Demand(formerly CylanceMDR On Demand)Aurora ProtectAurora Endpoint DefenseFeaturesOn');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'day threat prevention with immediate attack containment30% faster incident investigation and 90% reduction in alert fatigueLight');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'DrivenEndpoint SecurityAuroraTMEndpoint Security delivers market');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Day Data RetentionPlaybook AutomationManaged Endpoint SecurityAurora Managed Endpoint DefenseOn');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Proven AIZero');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'DemandAurora ProtectAurora Endpoint DefenseFeaturesRequest Help from SOCGuided RemediationOngoing Endpoint Health');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Focused Threat HuntingEndpoint SecurityManaged Endpoint SecurityAurora Protect(formerly CylanceProtect)FeaturesEndpoint Protection PlatformNext');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Focused Threat HuntingOnboardingSecure Your Endpoints Against Modern ThreatsBattle');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Weight, High');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'risk, and transform how you protect your organization');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'security', 'D', 'https://arcticwolf.com/solutions/industries/legal/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'based assignment of 16 compliance courses covering topics including:PCIHIPAAGDPRTitle IXFERPAAnti');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'life attacks. Our simulations include immediate and specific learning experiences following a simulated phishing ''click'' to remediate the risk.This pre');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'use phishing simulations based on real');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'packagedPhishing Simulationsand RemediationPrioritize impactful learning over mere click statisticsMeasure and reinforce employee awareness with automated, ready');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'fresh learning sessions are seamlessly delivered on a bi');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'based content across a range of highly targeted sectors with highly targeted employees.Incorporate cutting');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'data integrity and maintains the reliability of security alerts');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'human risk at your organization');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'security', 'a', 'https://arcticwolf.com/solutions/managed-security-awareness/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'based assignment of 16 compliance courses covering topics including:PCIHIPAAGDPRTitle IXFERPAAnti');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'life attacks. Our simulations include immediate and specific learning experiences following a simulated phishing ''click'' to remediate the risk.This pre');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'use phishing simulations based on real');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'packagedPhishing Simulationsand RemediationPrioritize impactful learning over mere click statisticsMeasure and reinforce employee awareness with automated, ready');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'fresh learning sessions are seamlessly delivered on a bi');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'based content across a range of highly targeted sectors with highly targeted employees.Incorporate cutting');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'data integrity and maintains the reliability of security alerts');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'human risk at your organization');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'security', 'y', 'https://arcticwolf.com/solutions/bundles/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearWarranty Options:$750K1');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearor$1.5M3');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'leading financial support for covered cyber events . The warranty can even be used to fund your organization’s cyber insurance deductible to minimize out');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'leading financial support to reduce out');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'pocket expenses after a covered eventMore DetailsMax Coverage by adding:Aurora Managed Endpoint DefenseWarranty Option:$100k3');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'tested IR Plan, and a prioritized response time SLAMore DetailsSecurity Operations WarrantyIndustry');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearWarranty Options:$500K1');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearRequesta BundlesDemoTransfer risk withbest');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'their risk profile and improve their insurability​');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'their insurability​');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'the frequency of successful attacks');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'security', 'a', 'https://arcticwolf.com/solutions/industries/financial-services/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'rich targets, mission');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'Bliley Act to the FFIEC Cybersecurity Assessment Tool to the Sarbanes');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'our threat surface');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'Risk, Increase ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'cyber risk exposure');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'security', 'S', 'https://arcticwolf.com/solutions/industries/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'force reportThe average cost of a data breach in manufacturing was $5.56 million in 2024, up 18% from the previous year.SOURCE: IBM InsightsCustomerTestimonialBeing a mid');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'privilege principlesSOURCE: 2024 IBM X');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'factor authentication or least');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'our threat surface');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'Risk, Increase ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'cyber risk exposure');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'security', 'd', 'https://arcticwolf.com/solutions/industries/manufacturing/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'force reportThe average cost of a data breach in manufacturing was $5.56 million in 2024, up 18% from the previous year.SOURCE: IBM InsightsCustomerTestimonialBeing a mid');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'privilege principlesSOURCE: 2024 IBM X');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'factor authentication or least');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'our threat surface');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'Risk, Increase ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'cyber risk exposure');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'security', 'C', 'https://arcticwolf.com/solutions/cloud-security-posture-management/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'Planning, Mitigated and more.Filter by status');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'based portal that provides visibility into the real');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'connected devices while cataloging your core infrastructure, equipment/peripherals, workstations, Internet of things (IoT) devices,and personal (e.g., tablets, cell phones) devices.Host');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'Based Vulnerability AssessmentThis capability extends visibility inside devicesthrough continuous host');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'based vulnerability management provided through Managed Risk.24x7 Monitoring24x7 monitoring for');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'facing assets to understand yourcompany’s digital footprint and quantify yourbusiness’s risk exposureInternal Vulnerability AssessmentArctic Wolf delivers continuous scanning of all your internal IP');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'our threat surface');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'Risk, Increase ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'cyber risk exposure');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'cloud', 'S', 'https://arcticwolf.com/solutions/cloud-detection-and-response/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'releases/cloud');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'enabled.84%84%of businesses are adopting a "multi');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'cloud" strategy.94%94%of enterprises today rely on at least one public cloud.Sources:brownglock.comflexera.comstratospherenetworks.cominfosecurity');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'MSP CybersecurityMSPs are in a unique position to protect their clients with strong cybersecurity services');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'your customers’ overall posture');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'the complexity associated with managing multiple vendors');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'their cybersecurity offerings to SMBs');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'general', 'c', 'https://arcticwolf.com/partners/managed-service-providers/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', '1MSP Volume OpportunitiesAccelerate your business opportunities by taking advantage of competitive volume');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'duplication services, along with robust account takeover risk detection and cloud security posture management.Learn MoreARCTIC WOLFManaged Security AwarenessDeliver fresh and timely co');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'world threat intel and industry trends, ensuring timely, relevant trainings, which MSPs can monitor through our multi');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'Time RemediationRapidly contain incidents and get detailed guidance on remediationOn');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'based pricing from Day');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', '1STRATEGICConciergeSecurity TeamThe Concierge Security Team is what sets Arctic Wolf apart');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'branded security awareness education to your customers through a completely automated, multi');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'leading security operationsBecome an MSP PartnerLogin to Partner PortalSecurity Operations for MSPsGenerate turnkey recurring revenue with industry');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'tenant portal with reporting — provides risk remediation guidance, security risk scoring, and configuration benchmarking.Offers asset inventory, tagging, criticality and de');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'MSP CybersecurityMSPs are in a unique position to protect their clients with strong cybersecurity services');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'your customers’ overall posture');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'the complexity associated with managing multiple vendors');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Managed Service Providers', 'their cybersecurity offerings to SMBs');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'general', 'u', 'https://arcticwolf.com/partners/oem-solutions/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'ready solutions. Those organizations know how important it is to have a high');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'consuming undertaking, especially for organizations if cybersecurity is not a core competency of their business or they are looking to expand their capabilities quickly with proven, market');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'the impact of a potential security incident, our team of 24×7 IR experts respond quickly to contain the threat');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'ransom demands');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'ransom demands and quicken the speed of recovery efforts');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'or Eliminate Ransom PaymentsOn average, Arctic Wolf Incident Response customers have seen a 92% reduction from the original demand request');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'general', 'I', 'https://arcticwolf.com/solutions/incident-response/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'end incident response support.Arctic Wolf customers have access to every emergency incident response service needed to get back to pre');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', '8429Arctic Wolf Resource Librarypr@arcticwolf.comTo contact Arctic Wolf for a non');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'emergency scenario, or to learn more about Incident Response please fill out the form.');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'incident business operations.Experiencing a Breach? Get Help NowBe Prepared with our IR RetainerA Partner You Can TrustArctic Wolf’s insurance');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'incident operations. With active monitoring, advanced forensics, business recovery, and threat actor negotiation expertise in');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'house, you’ll never need to slow your response to onboard a third party mid');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'kind Arctic Wolf Incident360 Retainer includes full IR coverage for any incident type. It provides customers with prioritized access to insurance');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'service incident response (IR) team has everything needed to stop an attack and quickly restore your organization to pre');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'functional expertise required to conduct rapid and thorough digital forensic investigations that include evidence collection and in');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'the impact of a potential security incident, our team of 24×7 IR experts respond quickly to contain the threat');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'ransom demands');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'ransom demands and quicken the speed of recovery efforts');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'or Eliminate Ransom PaymentsOn average, Arctic Wolf Incident Response customers have seen a 92% reduction from the original demand request');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'general', 'I', 'https://arcticwolf.com/solutions/incident-response-retainer/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'network portal that your team can easily access.PartnerOptionsAlready Working with an Arctic Wolf Partner?Arctic Wolf has a global community of industry');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'incident operations.');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'tested incident runbooks.Secure IR PortalStore all IR planning documents in a secure off');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'quality and approved by your insurance provider.Prioritized Response TimeGet your business back to a pre');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', '7?Yes. Arctic Wolf’s incident response services are available 24');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Hour Response Time SLA​$325 Hourly IR Rate​IR Planner​Incident');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'hour response time SLA.Security Posture HardeningMap your security posture to industry frameworks to identify gaps and track improvements.Incident RunbooksPrepare for severe cyber attacks with battle');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'incident state faster with a 3');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Specific RunbooksCyber Resilience AssessmentBuyJumpStart RetainerIncident360RetainerJumpStart ​RetainerFeaturesCoverage for One Incident​3');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Approved IR FirmTrust that the IR services your organization receives will be high');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'your cyber insurability');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'security', 'r', 'https://arcticwolf.com/solutions/industries/healthcare/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'edge defenses.Threat actors know all of this, which is why healthcare is such a tempting target for phishing, ransomware, spear');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'your cyber insurability');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'general', 'i', 'https://arcticwolf.com/solutions/managed-detection-and-response/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'time threat campaign bulletinsExternal Ingestion (STIX/TAXII)And more!Explore Threat IntelligenceArctic Wolf®Security Operations WarrantyTHE PACK HAS YOUR BACKGet the industry');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'your cyber insurability');
INSERT INTO services (vendor_id, service_name, category, description, url, pricing) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'general', 'c', 'https://arcticwolf.com/solutions/cyber-jumpstart/', '');
INSERT INTO service_features (vendor_id, service_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'evolving threat landscape.Close security gaps with in');
INSERT INTO service_benefits (vendor_id, service_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'your cyber insurability');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'security', 'a', 'https://arcticwolf.com/solutions/industries/government/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsSchool DistrictsHigher EducationCities & CountiesLocal GovernmentState AgenciesHealthcare OrganizationsReligious OrganizationsNon');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsState GovernmentsLocal GovernmentsHigher EducationK');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', '12 EducationNon');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'Profit OrganizationsTexas State AgenciesCountiesLocal GovernmentPublic Education(Out of State with ICC Agreements)Higher EducationCommunity CollegesK');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'productivity at a lower cost');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cybersecurity for State and Local Government', 'in attacks to government and civic organizations in 2024 over the prior year');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'security', 'A', 'https://arcticwolf.com/solutions/endpoint-security/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'DrivenEndpoint SecurityAuroraTMEndpoint Security delivers market');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Day Data RetentionPlaybook AutomationManaged Endpoint SecurityAurora Managed Endpoint DefenseOn');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'DemandAurora ProtectAurora Endpoint DefenseFeaturesRequest Help from SOCGuided RemediationOngoing Endpoint Health');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Focused Threat HuntingEndpoint SecurityManaged Endpoint SecurityAurora Protect(formerly CylanceProtect)FeaturesEndpoint Protection PlatformNext');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Day Data RetentionPlaybook AutomationManaged Endpoint SecurityAurora Managed Endpoint DefenseOn');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Demand(formerly CylanceMDR On Demand)Aurora ProtectAurora Endpoint DefenseFeaturesOn');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Focused Threat HuntingOnboardingSecure Your Endpoints Against Modern ThreatsBattle');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Proven AIZero');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'day threat prevention with immediate attack containment30% faster incident investigation and 90% reduction in alert fatigueLight');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'Weight, High');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'on experience that allows you to see our market');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'class endpoint security to a full security operations program. By operationalizing endpoint technology, customers can shift from a tools');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'risk, and transform how you protect your organization');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'market-leading AI-driven prevention, detection, and response, stopping threats before they disrupt your business');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'powerful, AI-driven defense against modern threats');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Endpoint Security', 'protection, detection, and response as well as threat hunting capabilities');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'general', 't', 'https://arcticwolf.com/partners/solution-providers/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'tenant portal with reporting — provides risk remediation guidance, security risk scoring, and configuration benchmarking.Offers asset inventory, tagging, criticality and de');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'duplication services, along with robust account takeover risk detection and cloud security posture management.Learn MoreARCTIC WOLFManaged Security AwarenessDeliver fresh and timely co');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'branded security awareness education to your customers through a completely automated, multi');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'world threat intel and industry trends, ensuring timely, relevant trainings, which MSPs can monitor through our multi');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'tenant dashboard.Learn MoreQuestions? Contact us todayOur cybersecurity experts are ready to help. Click the button to fill out a form and we’ll get in touch with you.LET''S TALK');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'the complexity associated with managing multiple vendors');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf for Solution Providers', 'AI-driven prevention, detection, and response to stop endpoint threats before they disrupt business');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'security', 'S', 'https://arcticwolf.com/solutions/industries/legal/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'fresh learning sessions are seamlessly delivered on a bi');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'packagedPhishing Simulationsand RemediationPrioritize impactful learning over mere click statisticsMeasure and reinforce employee awareness with automated, ready');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'use phishing simulations based on real');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'life attacks. Our simulations include immediate and specific learning experiences following a simulated phishing ''click'' to remediate the risk.This pre');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'based content across a range of highly targeted sectors with highly targeted employees.Incorporate cutting');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'based assignment of 16 compliance courses covering topics including:PCIHIPAAGDPRTitle IXFERPAAnti');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'data integrity and maintains the reliability of security alerts');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'human risk at your organization');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'relevant and engaging content based on the latest threats and attack methods');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Legal Industry Cybersecurity', 'awareness lessons via email for quick and convenient access');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'security', 'S', 'https://arcticwolf.com/solutions/managed-security-awareness/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'fresh learning sessions are seamlessly delivered on a bi');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'packagedPhishing Simulationsand RemediationPrioritize impactful learning over mere click statisticsMeasure and reinforce employee awareness with automated, ready');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'use phishing simulations based on real');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'life attacks. Our simulations include immediate and specific learning experiences following a simulated phishing ''click'' to remediate the risk.This pre');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'based content across a range of highly targeted sectors with highly targeted employees.Incorporate cutting');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'based assignment of 16 compliance courses covering topics including:PCIHIPAAGDPRTitle IXFERPAAnti');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'data integrity and maintains the reliability of security alerts');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'human risk at your organization');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'relevant and engaging content based on the latest threats and attack methods');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Security Awareness', 'awareness lessons via email for quick and convenient access');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'security', 'S', 'https://arcticwolf.com/solutions/bundles/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'tested IR Plan, and a prioritized response time SLAMore DetailsSecurity Operations WarrantyIndustry');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'leading financial support to reduce out');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'pocket expenses after a covered eventMore DetailsMax Coverage by adding:Aurora Managed Endpoint DefenseWarranty Option:$100k3');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearWarranty Options:$500K1');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearWarranty Options:$750K1');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearor$1.5M3');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'yearRequesta BundlesDemoTransfer risk withbest');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'leading financial support for covered cyber events . The warranty can even be used to fund your organization’s cyber insurance deductible to minimize out');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'their insurability​');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'the frequency of successful attacks');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Security Operations Bundles', 'their risk profile and improve their insurability​');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'security', 'S', 'https://arcticwolf.com/solutions/industries/financial-services/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'rich targets, mission');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'Bliley Act to the FFIEC Cybersecurity Assessment Tool to the Sarbanes');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Financial Industry Cybersecurity', 'the tools and expertise to continually monitor our environment and alert on these threats');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'security', 'S', 'https://arcticwolf.com/solutions/industries/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'factor authentication or least');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'privilege principlesSOURCE: 2024 IBM X');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'force reportThe average cost of a data breach in manufacturing was $5.56 million in 2024, up 18% from the previous year.SOURCE: IBM InsightsCustomerTestimonialBeing a mid');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Meeting Industry Cybersecurity and Regulatory Requirements', 'the tools and expertise to continually monitor our environment and alert on these threats');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'security', 'S', 'https://arcticwolf.com/solutions/industries/manufacturing/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'factor authentication or least');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'privilege principlesSOURCE: 2024 IBM X');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'force reportThe average cost of a data breach in manufacturing was $5.56 million in 2024, up 18% from the previous year.SOURCE: IBM InsightsCustomerTestimonialBeing a mid');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing Industry Cybersecurity', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'security', 'S', 'https://arcticwolf.com/solutions/cloud-security-posture-management/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'cloud', 'S', 'https://arcticwolf.com/solutions/cloud-detection-and-response/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'releases/cloud');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'enabled.84%84%of businesses are adopting a "multi');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'cloud" strategy.94%94%of enterprises today rely on at least one public cloud.Sources:brownglock.comflexera.comstratospherenetworks.cominfosecurity');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cloud Detection and Response', 'consistent performance');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'general', 'a', 'https://arcticwolf.com/partners/oem-solutions/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'consuming undertaking, especially for organizations if cybersecurity is not a core competency of their business or they are looking to expand their capabilities quickly with proven, market');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'ready solutions. Those organizations know how important it is to have a high');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'OEM Solutions', 'consistent performance');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'general', 'I', 'https://arcticwolf.com/solutions/incident-response/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'service incident response (IR) team has everything needed to stop an attack and quickly restore your organization to pre');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'incident business operations.Experiencing a Breach? Get Help NowBe Prepared with our IR RetainerA Partner You Can TrustArctic Wolf’s insurance');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'kind Arctic Wolf Incident360 Retainer includes full IR coverage for any incident type. It provides customers with prioritized access to insurance');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'end incident response support.Arctic Wolf customers have access to every emergency incident response service needed to get back to pre');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'incident operations. With active monitoring, advanced forensics, business recovery, and threat actor negotiation expertise in');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'house, you’ll never need to slow your response to onboard a third party mid');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'functional expertise required to conduct rapid and thorough digital forensic investigations that include evidence collection and in');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', '8429Arctic Wolf Resource Librarypr@arcticwolf.comTo contact Arctic Wolf for a non');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'emergency scenario, or to learn more about Incident Response please fill out the form.');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'ransom demands');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'or Eliminate Ransom PaymentsOn average, Arctic Wolf Incident Response customers have seen a 92% reduction from the original demand request');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'the impact of a potential security incident, our team of 24×7 IR experts respond quickly to contain the threat');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response', 'ransom demands and quicken the speed of recovery efforts');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', 'platform', 'T', 'https://arcticwolf.com/aurora-platform/alpha-ai/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', 'AI Relationship For Security Operations SuccessIn this report, you’ll get exclusive insights into our survey of nearly 2,000 global organizations to help you navigate the human');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', 'All numbers are approximateReady to Get Started?Unlock the future of Security Operations today with Alpha AIGeneral Questions1-888-272-8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', 'a new approach to IR retainers that provides organizations with advanced incident readiness activities without having to sacrifice the ability to respond to a severe security event');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Alpha AI', 'security operations as a concierge service');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'general', 'I', 'https://arcticwolf.com/solutions/incident-response-retainer/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Approved IR FirmTrust that the IR services your organization receives will be high');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'quality and approved by your insurance provider.Prioritized Response TimeGet your business back to a pre');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'incident state faster with a 3');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'hour response time SLA.Security Posture HardeningMap your security posture to industry frameworks to identify gaps and track improvements.Incident RunbooksPrepare for severe cyber attacks with battle');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'tested incident runbooks.Secure IR PortalStore all IR planning documents in a secure off');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'network portal that your team can easily access.PartnerOptionsAlready Working with an Arctic Wolf Partner?Arctic Wolf has a global community of industry');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Hour Response Time SLA​$325 Hourly IR Rate​IR Planner​Incident');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'Specific RunbooksCyber Resilience AssessmentBuyJumpStart RetainerIncident360RetainerJumpStart ​RetainerFeaturesCoverage for One Incident​3');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'incident operations.');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', '7?Yes. Arctic Wolf’s incident response services are available 24');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'service portalor contactingonline');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'help@arcticwolf.com.How can I change my user amount?You can update your user amount at any time prior to the trial ending by working with your customer success manager or contactingonline');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'help@arcticwolf.com.When and how do I cancel?You can cancel at any time through theself');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'service portalor contactingonline');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'help@arcticwolf.com.What do you mean by engage?Employee participation, or engagement, is critical to your awareness program. Arctic Wolf provides no');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'a new approach to IR retainers that provides organizations with advanced incident readiness activities without having to sacrifice the ability to respond to a severe security event');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Incident360 Retainer', 'security operations as a concierge service');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'security', 'S', 'https://arcticwolf.com/solutions/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'platform', 'S', 'https://arcticwolf.com/aurora-platform/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'leading open XDR platformHOW IT WORKSCollectSee the complete picture with broad visibility, unlimited event data, and on');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'demand access to your data.EnrichThreat IntelCorrelates all events with industry');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'streams of security observations.Join Arctic Wolf’s Dan Schiappa, Chief Product Officer, and Ian McShane, Vice President of Product, as they share their vision for AI in the context of the industry');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'alert fatigue');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'false positives');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'our unique personalized protection for your organization');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Aurora Platform', 'the tools and expertise to continually monitor our environment and alert on these threats');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'security', 'f', 'https://arcticwolf.com/solutions/industries/healthcare/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'edge defenses.Threat actors know all of this, which is why healthcare is such a tempting target for phishing, ransomware, spear');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare Cybersecurity', 'the tools and expertise to continually monitor our environment and alert on these threats');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'general', 'S', 'https://arcticwolf.com/solutions/managed-detection-and-response/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'time threat campaign bulletinsExternal Ingestion (STIX/TAXII)And more!Explore Threat IntelligenceArctic Wolf®Security Operations WarrantyTHE PACK HAS YOUR BACKGet the industry');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Managed Detection and Response (MDR)', 'the tools and expertise to continually monitor our environment and alert on these threats');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'tool', 'I', 'https://arcticwolf.com/interactive-insights/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'leading Security Operations workflow remediated a ransomware attack on a local government organization.View TimelineOther Not');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'SoInteractive Content You Might LikeResource LibraryReady ToTalk To An Arctic Wolf ExpertOur cybersecurity experts are ready to help. Fill out the form and we’ll get in touch with you.');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'Risk, Increase ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'cyber risk exposure');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'our threat surface');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'ResilienceGain a comprehensive understanding of your organization’s digital risks for more effective risk assessment and management with Arctic Wolf Managed Risk');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'timely critical');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Arctic Wolf Interactive Tools', 'continuous scanning of all your internal IP-connected devices while cataloging your core infrastructure, equipment/peripherals, workstations, Internet of things (IoT) devices,and personal (e');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'general', 'S', 'https://arcticwolf.com/solutions/managed-risk/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', '8429Arctic Wolf Resource Librarypr@arcticwolf.com');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Solutions', 'cloud-related security incidents due to misconfiguration by 80%');
INSERT INTO products (vendor_id, product_name, category, description, url, pricing, target_audience, requirements, deployment, support) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'general', 'r', 'https://arcticwolf.com/solutions/cyber-jumpstart/', '', '', '', '', '');
INSERT INTO product_features (vendor_id, product_name, feature) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'evolving threat landscape.Close security gaps with in');
INSERT INTO product_benefits (vendor_id, product_name, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Cyber Jumpstart', 'your cyber insurability');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Aws');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Azure');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Gcp');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Go');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Java');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Javascript');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Linux');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Macos');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'React');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Rust');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Swift');
INSERT INTO technology_stack (vendor_id, technology) VALUES ('arctic_wolf_we_make_security_work', 'Windows');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Automotive');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Banking');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Education');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Energy');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Financial');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Government');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Healthcare');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Insurance');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Legal');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Manufacturing');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Real Estate');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Retail');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Technology');
INSERT INTO industries (vendor_id, industry) VALUES ('arctic_wolf_we_make_security_work', 'Telecommunications');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'gestützte Cybersecurity');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'time monitoring of your entire endpoint environment, plus powerful AI');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'raportissaLue lisääNimetty 2024 IDC MarketScapessa Worldwide Managed Detection and Response');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'Firestone Grand Prix of St. PetersburgMAR 23');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'pocket costs while potentially gaining access to lower premiums and more favorable policy terms.Learn MoreExperienced Incident ResponseArctic Wolf’s insurance');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'Profit OrganizationsState GovernmentsLocal GovernmentsHigher EducationK');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'tested incident runbooks.Secure IR PortalStore all IR planning documents in a secure off');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'DSS REQUIREMENTS1PCI');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'Demand WebinarOperationalizing the AI');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'premises and in the cloudProvide real');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'leading open XDR platformHOW IT WORKSCollectSee the complete picture with broad visibility, unlimited event data, and on');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'AI relationship in security operations. This report reveals key findings on AI adoption, attitudes towards AI, and the importance of human');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'Force AttackWhat Is a Brute');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', '6  Cyber Security  Physical Security of BES Cyber Systems6CIP');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'facing, known vulnerabilities.Security Project GuidesInsureds can close their security gaps with in');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'Incident Response: Establishing well');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'class security operations with the push of a button.For more information about Arctic Wolf,contact us.Learn More');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'platformOns open XDR');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', 'leading security operations.Learn MoreARCTIC WOLF FORSolution ProvidersWith recurring revenue, ample upsell opportunities, and a 100% channel go');
INSERT INTO general_features (vendor_id, feature) VALUES ('arctic_wolf_we_make_security_work', '592305066836Windows 10 Version 1809 for 32');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'the likelihood of insurability');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Attack FrequencyIncident Response JumpStart RetainerLock in a 1-hour response time and preferred rates from an insurance-approved IR team');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'your cyber insurance risk profile');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'cybersecurity practices, and creates a common language for internal and external communication of cybersecurity issues');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'ransom demands');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'accessibility to cyber protection, including our award-winningLog4Shell Deep Scan Tool');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'your cyber risk while improving your security posture');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'your risk profile, increase the likelihood of insurability, and potentially lower your rates');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'ransom demands and quicken the speed of recovery efforts');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'risk, and transform how you protect your organization');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'MSP CybersecurityMSPs are in a unique position to protect their clients with strong cybersecurity services');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'your customers’ overall posture');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'service performance and to learn about visitors to the Arctic Wolf website(s)');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'their security posture');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'their cyber risk');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'the impact of a potential security incident, our team of 24×7 IR experts respond quickly to contain the threat');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'ransom demands and speed up recovery, while supporting our digital forensics teams');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'their risk profile and improve their insurability​');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'Risk and Understand Insurability with Cyber JumpStartStart your security journey today for freeGet actionable guidance on how to strengthen your cyber resilience and improve your cyber insurability');
INSERT INTO general_benefits (vendor_id, benefit) VALUES ('arctic_wolf_we_make_security_work', 'cyber risk exposure');
INSERT INTO certifications (vendor_id, certification) VALUES ('arctic_wolf_we_make_security_work', 'What You Need to KnowCybersecurity Compliance GuideKRITISIT Security Act 2');

