# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.utils import nowdate, add_days
import frappe
from frappe import _
from frappe.model.document import Document

class Meeting(Document):
	def validate(self):
		"""Set missing names and warn if duplicate"""
		found = []
		for attendee in self.attendee:
			if not attendee.full_name:
				attendee.full_name = get_full_name(attendee.attendee)

			if attendee.attendee in found:
				frappe.throw(_("Attendee {0} entered twice").format(attendee.attendee))

			found.append(attendee.attendee)




@frappe.whitelist()			
def get_full_name(attendee):
	user = frappe.get_doc("User",attendee)

	#concatenates by space if it has a value
	return "".join(filter(None, [user.first_name, user.middle_name, user.last_name]))


@frappe.whitelist()
def send_invitation_email(meeting):
	frappe.errprint(meeting)
	meeting = frappe.get_doc("Meeting", meeting)
	meeting.check_permission("email")

	if meeting.status == "Planned":
		frappe.sendmail(
			recipients=[d.attendee for d in meeting.attendee],
			sender=frappe.session.user,
			#subject=meeting.title,
			message=meeting.invitation_message,
			reference_doctype=meeting.doctype,
			reference_name=meeting.name
		)

		meeting.status = "Invitation Sent"
		meeting.save()

		frappe.msgprint(_("Invitation Sent"))

	else:
		frappe.msgprint(_("Meeting Status must be 'Planned'"))


@frappe.whitelist()
def get_meetings(start, end):
	if not frappe.has_permission("Meeting", "read"):
		raise frappe.PermissionError

	return frappe.db.sql("""select
		timestamp(`date`, from_time) as start,
		timestamp(`date`, to_time) as end,
		name,
		title,
		status,
		0 as all_day
	from `tabMeeting`
	where `date` between %(start)s and %(end)s""", {
		"start": start,
		"end": end
	}, as_dict=True)

def make_orientation_meeting(doc, method):
	"""Create an orientation meeting when a new User is added"""

	nm = frappe.new_doc("Meeting")
	nm.doctype = "Meeting"
	nm.title = "Orientation for {0}".format(doc.first_name),
	nm.date = add_days(nowdate(), 1),
	nm.from_time = "09:00",
	nm.to_time = "09:30",
	nm.status = "Planned"
	
	nm.save(ignore_permissions=True)	

	frappe.msgprint(_("Orientation meeting created"))