#!/usr/bin/env python3
"""
PyCon25 Hackathon: Intelligent Support Ticket Assignment System
Author: Aakash Khandelwal
Date: September 2025

This system assigns support tickets to agents based on:
1. Skill matching using NLP techniques
2. Priority scoring based on urgency keywords
3. Workload balancing
4. Agent experience and availability
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

class IntelligentTicketAssignmentSystem:
    """
    Advanced ticket assignment system that optimally routes support requests
    to the most suitable agents based on multiple criteria.
    """

    def __init__(self):
        # Skill keyword mappings for intelligent text analysis
        self.skill_keywords = {
            'VPN_Troubleshooting': ['vpn', 'virtual private network', 'tunnel', 'authentication error'],
            'Networking': ['network', 'connectivity', 'ping', 'switch', 'router', 'outage', 'dns'],
            'Hardware_Diagnostics': ['hardware', 'laptop', 'desktop', 'boot', 'bios', 'fan', 'overheating', 'port', 'usb', 'monitor', 'projector'],
            'Laptop_Repair': ['laptop', 'battery', 'charging', 'screen', 'keyboard', 'fan'],
            'Microsoft_365': ['outlook', 'microsoft 365', 'm365', 'email', 'onedrive', 'teams'],
            'Active_Directory': ['active directory', 'ad', 'account', 'user account', 'domain', 'login', 'password reset', 'sso', 'saml'],
            'Database_SQL': ['database', 'sql server', 'query', 'backup', 'connection timeout'],
            'Network_Security': ['security', 'firewall', 'intrusion', 'breach', 'malicious'],
            'Endpoint_Security': ['malware', 'antivirus', 'trojan', 'phishing', 'security'],
            'Cloud_Azure': ['azure', 'app service', 'cloud'],
            'Cloud_AWS': ['aws', 'cloud'],
            'Printer_Troubleshooting': ['printer', 'printing'],
            'SharePoint_Online': ['sharepoint', 'collaboration', 'site'],
            'Voice_VoIP': ['voip', 'phone', 'call'],
            'Web_Server_Apache_Nginx': ['website', 'web server', '502', '500', '404'],
            'Windows_OS': ['windows', 'desktop', 'pc'],
            'Mac_OS': ['mac', 'macos', 'macbook'],
            'Linux_Administration': ['linux', 'ubuntu', 'samba', 'permission'],
            'DevOps_CI_CD': ['jenkins', 'ci/cd'],
            'Virtualization_VMware': ['vm', 'virtual machine', 'vmware'],
            'API_Troubleshooting': ['api'],
            'DNS_Configuration': ['dns'],
            'SSL_Certificates': ['ssl', 'certificate'],
            'Phishing_Analysis': ['phishing'],
            'SIEM_Logging': ['siem', 'log'],
            'Identity_Management': ['identity', 'sso'],
            'SaaS_Integrations': ['saas', 'integration'],
            'Firewall_Configuration': ['firewall'],
            'Switch_Configuration': ['switch'],
            'Routing_Protocols': ['routing'],
            'Network_Monitoring': ['monitoring'],
            'Endpoint_Management': ['endpoint'],
            'PowerShell_Scripting': ['powershell'],
            'Software_Licensing': ['license'],
            'Python_Scripting': ['python'],
            'Kubernetes_Docker': ['kubernetes', 'docker'],
            'ETL_Processes': ['etl'],
            'Data_Warehousing': ['data warehouse'],
            'PowerBI_Tableau': ['powerbi', 'tableau'],
            'Cisco_IOS': ['cisco'],
            'Network_Cabling': ['cable', 'cabling']
        }

        # Priority detection keywords
        self.priority_keywords = {
            'critical': ['critical', 'business-critical', 'down', 'outage', 'not working', 'failure', 'failed', 'crash', 'urgent', 'immediate'],
            'high': ['high', 'security', 'breach', 'malware', 'slow', 'performance', 'locked', 'cannot', 'unable', 'broken'],
            'medium': ['medium', 'sync', 'access', 'permission', 'configuration'],
            'low': ['request', 'setup', 'new user', 'license', 'standard', 'routine']
        }

    def extract_required_skills(self, text: str) -> List[str]:
        """Extract relevant skills from ticket text using keyword matching"""
        text_lower = text.lower()
        relevant_skills = []

        for skill, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    relevant_skills.append(skill)
                    break

        return list(set(relevant_skills))

    def calculate_priority_score(self, text: str) -> int:
        """Calculate priority score based on urgency indicators (1-10)"""
        text_lower = text.lower()

        # Critical priority indicators
        for keyword in self.priority_keywords['critical']:
            if keyword in text_lower:
                return 10

        # High priority indicators
        for keyword in self.priority_keywords['high']:
            if keyword in text_lower:
                return 8

        # Medium priority indicators
        for keyword in self.priority_keywords['medium']:
            if keyword in text_lower:
                return 5

        # Low priority indicators
        for keyword in self.priority_keywords['low']:
            if keyword in text_lower:
                return 2

        return 6  # Default medium priority

    def calculate_agent_score(self, agent: Dict, required_skills: List[str], 
                            priority_score: int, current_load: int) -> Dict:
        """
        Calculate comprehensive agent suitability score

        Scoring components:
        - Skill matching (0-100): How well agent skills match ticket requirements
        - Experience factor (0-20): Agent experience level
        - Workload penalty (0-30): Lower workload = higher score
        - Availability bonus (0-10): Agent availability status
        - Priority bonus (0-5): High priority tickets get experienced agents
        """

        # 1. Skill matching score
        skill_scores = []
        for skill in required_skills:
            if skill in agent['skills']:
                skill_scores.append(agent['skills'][skill])
            else:
                skill_scores.append(0)

        avg_skill_score = sum(skill_scores) / len(skill_scores) if skill_scores else 0
        skill_match_score = avg_skill_score * 10  # Scale to 0-100

        # 2. Experience factor
        experience_score = min(agent['experience_level'] * 1.5, 20)

        # 3. Workload penalty
        max_reasonable_load = 5
        workload_score = max(0, (max_reasonable_load - current_load) * 6)

        # 4. Availability bonus
        availability_score = 10 if agent['availability_status'] == 'Available' else 0

        # 5. Priority bonus for critical tickets
        priority_bonus = priority_score * 0.5 if priority_score >= 8 else 0

        total_score = (skill_match_score + experience_score + 
                      workload_score + availability_score + priority_bonus)

        return {
            'total_score': total_score,
            'skill_score': skill_match_score,
            'experience_score': experience_score,
            'workload_score': workload_score,
            'availability_score': availability_score,
            'priority_bonus': priority_bonus
        }

    def create_assignment_rationale(self, agent: Dict, required_skills: List[str], 
                                  score_info: Dict, priority: int) -> str:
        """Generate human-readable assignment rationale"""

        # Find agent's relevant skills
        relevant_skills = []
        for skill in required_skills:
            if skill in agent['skills']:
                relevant_skills.append(f"'{skill}' ({agent['skills'][skill]})")

        skill_text = ", ".join(relevant_skills[:3])  # Limit to top 3 skills

        rationale_parts = []

        if relevant_skills:
            rationale_parts.append(
                f"Assigned to {agent['name']} ({agent['agent_id']}) "
                f"based on expertise in {skill_text}"
            )
        else:
            rationale_parts.append(
                f"Assigned to {agent['name']} ({agent['agent_id']}) "
                f"based on experience level ({agent['experience_level']})"
            )

        if score_info['workload_score'] > 15:
            rationale_parts.append("and lower current workload")

        if priority >= 8:
            rationale_parts.append("High priority ticket requiring immediate attention")

        return ". ".join(rationale_parts) + "."

    def assign_tickets(self, agents_data: List[Dict], tickets_data: List[Dict]) -> List[Dict]:
        """
        Main assignment algorithm

        Process:
        1. Analyze each ticket for required skills and priority
        2. Sort tickets by priority (high priority first) and age
        3. For each ticket, calculate scores for all agents
        4. Assign to highest scoring agent
        5. Update agent workload for subsequent assignments
        """

        # Track dynamic agent workloads during assignment
        agent_loads = {agent['agent_id']: agent['current_load'] for agent in agents_data}

        # Prepare tickets with metadata
        tickets_with_metadata = []
        for ticket in tickets_data:
            text = ticket['title'] + " " + ticket['description']
            priority = self.calculate_priority_score(text)
            required_skills = self.extract_required_skills(text)

            tickets_with_metadata.append({
                'ticket': ticket,
                'priority': priority,
                'required_skills': required_skills
            })

        # Sort by priority (highest first) then by timestamp (oldest first)
        tickets_with_metadata.sort(
            key=lambda x: (-x['priority'], x['ticket']['creation_timestamp'])
        )

        assignments = []

        # Process each ticket
        for ticket_info in tickets_with_metadata:
            ticket = ticket_info['ticket']
            required_skills = ticket_info['required_skills']
            priority = ticket_info['priority']

            # Calculate scores for all agents
            agent_scores = []
            for agent in agents_data:
                current_load = agent_loads[agent['agent_id']]
                score_info = self.calculate_agent_score(
                    agent, required_skills, priority, current_load
                )

                agent_scores.append({
                    'agent': agent,
                    'score_info': score_info
                })

            # Sort by total score (highest first)
            agent_scores.sort(key=lambda x: x['score_info']['total_score'], reverse=True)

            # Assign to best scoring agent
            best_match = agent_scores[0]
            best_agent = best_match['agent']
            best_score = best_match['score_info']

            # Update agent's workload for subsequent assignments
            agent_loads[best_agent['agent_id']] += 1

            # Create assignment record
            assignment = {
                "ticket_id": ticket['ticket_id'],
                "title": ticket['title'],
                "assigned_agent_id": best_agent['agent_id'],
                "rationale": self.create_assignment_rationale(
                    best_agent, required_skills, best_score, priority
                )
            }

            assignments.append(assignment)

        return assignments


def main():
    """Main execution function"""

    # Load input data
    try:
        with open('dataset.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: dataset.json not found!")
        return

    # Initialize assignment system
    assignment_system = IntelligentTicketAssignmentSystem()

    # Generate assignments
    print("🚀 Processing ticket assignments...")
    assignments = assignment_system.assign_tickets(data['agents'], data['tickets'])

    # Prepare output
    output_data = {
        "sample_output": assignments
    }

    # Save results
    with open('output_result.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    # Print summary
    print(f"✅ Successfully assigned {len(assignments)} tickets")
    print(f"📄 Results saved to: output_result.json")

    # Quick analysis
    agent_assignment_counts = {}
    for assignment in assignments:
        agent_id = assignment['assigned_agent_id']
        agent_assignment_counts[agent_id] = agent_assignment_counts.get(agent_id, 0) + 1

    print("\n📊 Assignment Distribution:")
    for agent_id, count in sorted(agent_assignment_counts.items()):
        agent_name = next(agent['name'] for agent in data['agents'] if agent['agent_id'] == agent_id)
        print(f"  {agent_id} ({agent_name}): {count} tickets")


if __name__ == "__main__":
    main()
