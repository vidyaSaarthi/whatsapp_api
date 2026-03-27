from database import SessionLocal
import models
from tabulate import tabulate

import os
import time
import glob


def show_student_list(view_campaign_flag = True, campaign_name = 'NO'):
    db = SessionLocal()
    try:
        if campaign_name == "NO":
            students = db.query(models.Student).all()
        else:

            # Filter the query directly at the database level
            students = db.query(models.Student).filter(
                models.Student.campaign_tags == campaign_name
            ).all()


        if not students:
            print("No students found in the database.")
            return

        # 1. Group students by their campaign tag
        campaign_groups = {}

        for s in students:
            tag = s.campaign_tags.strip() if s.campaign_tags else "Unassigned / Organic"
            if tag not in campaign_groups:
                campaign_groups[tag] = []
            campaign_groups[tag].append(s)

            sorted_campaigns = sorted(
                campaign_groups.items(),
                key=lambda x: len(x[1]),
                reverse=True
            )

        print(f"\n=========================================")
        print(f" 📋 VidyaSaarthi Students By Campaign")
        print(f"=========================================\n")

        # 2. Loop through each campaign and print its table + specific summary
        for campaign_name, student_list in sorted_campaigns:
            if view_campaign_flag:
                print(f"🎯 CAMPAIGN: {campaign_name.upper()}")

            table_data = []
            campaign_subscribed_count = 0  # 🚨 NEW: Counter just for this campaign

            for s in student_list:
                if s.opt_in_status:
                    status = "✅ Subscribed"
                    campaign_subscribed_count += 1
                else:
                    status = "❌ Unsubscribed"

                date_str = s.created_at.strftime('%Y-%m-%d') if s.created_at else "Unknown"
                display_name = s.name if s.name else "Unknown"

                table_data.append([display_name, s.phone_number, status, date_str])

            headers = ["Name", "Phone Number", "Opt-in Status", "Joined Date"]
            if view_campaign_flag:
                print(tabulate(table_data, headers=headers, tablefmt="grid"))

            # 🚨 NEW: Print the specific summary for this campaign right under its table
            campaign_total = len(student_list)
            print(f"📌 {campaign_name} Summary: {campaign_total} Total | {campaign_subscribed_count} Subscribed")
            if view_campaign_flag:
                print("\n" + "-" * 45 + "\n")  # Visual separator between campaigns

        # 3. Overall System Summary
        total_count = len(students)
        subscribed_count = sum(1 for s in students if s.opt_in_status)

        print(f"📊 SYSTEM SUMMARY")
        print(f"-----------------------------------------")
        print(f"Total Unique Campaigns: {len(campaign_groups)}")
        print(f"Total Students: {total_count} | Active Subscribers: {subscribed_count}")
        print(f"=========================================\n")

    except Exception as e:
        print(f"Error fetching students: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # show_student_list(view_campaign_flag = False)
    # show_student_list(view_campaign_flag=True)
    show_student_list(view_campaign_flag=True, campaign_name = 'Aakash - Kaithal Branch')