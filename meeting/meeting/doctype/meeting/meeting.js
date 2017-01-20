// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Meeting", {
	send_email: function(frm) {
		if (frm.doc.status==="Planned") {
			console.log("inside Planned")
			frappe.call({
				method: "meeting.meeting.doctype.meeting.meeting.send_invitation_email",
				args: {
					"meeting": frm.doc.name
				}
			});
		}
	},
});


frappe.ui.form.on('Meeting Attendee', {
	attendee: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		console.log(d.attendee)
		if (d.attendee) {
			//if attendee get full name
			frappe.call({
				method: "meeting.meeting.doctype.meeting.meeting.get_full_name",
				args:{
					"attendee": d.attendee
				},
				callback: function(r){
					console.log(r.message)
					frappe.model.set_value(cdt, cdn, "full_name",r.message);
				}
			})
		}
	}

});

