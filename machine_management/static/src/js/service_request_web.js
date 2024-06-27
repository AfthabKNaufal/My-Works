/** @odoo-module */

import PublicWidget from "@web/legacy/js/public/public_widget";
import { PyDate, PyTimeDelta } from "@web/core/py_js/py_date";
import { jsonrpc } from "@web/core/network/rpc_service";

PublicWidget.registry.TableColumnValue = PublicWidget.Widget.extend({
    selector: '.table_form',
    events: {
        'click .edit_button': '_TableValues',

    },
    _TableValues: function (ev){
          var row = $(ev.target).parent().parent()
          var id_machine = ev.target.id
          console.log(row)
          var row_machine = (row.find("td:eq(0)").text())
          var row_serial = (row.find("td:eq(1)").text())
          var row_customer = (row.find("td:eq(2)").text())
          var row_date= (row.find("td:eq(3)").text())
          var row_frequency = (row.find("td:eq(4)").text())
          var row_internal = (row.find("td:eq(5)").text())
          var obj={}
          obj.machine=row_machine
          obj.serial=row_serial
          obj.customer=row_customer
          obj.date=row_date
          obj.frequency=row_frequency
          obj.row_internal=row_internal
          $('#edit-modal').modal('toggle')
          $('#machine_modal').val(obj.machine)
          $('#serial_number').val(obj.serial)
          $('#customer_modal').val(obj.customer)
          $('#date_modal').val(obj.date)
          $('#select_frequency').val(obj.frequency)
          $('#id_machine').val(id_machine)
          $("#internal_modal").val(obj.row_internal)

    },

});

PublicWidget.registry.FieldValue = PublicWidget.Widget.extend({
    selector:'.modal-content',
    events: {
    'click #update': '_UpdateValue',
    'click #date_modal': '_ModalSetDate'
    },
    _UpdateValue: function(ev){
    var year_val = new Date($('#date_modal').val());
    var year = year_val.getFullYear();
    var month = year_val.getMonth();
    var date = year_val.getDate();
    if (year <= new Date().getFullYear() && month <= new Date().getMonth() && date < new Date().getDate())
    {
    alert("Cannot place a service request on past!")
    return false;
    }
    if (year > new Date().getFullYear() + 2){
    alert("Maximum up to above 2 years request can only be pre requested ")
    return false;
    }
    },
    _ModalSetDate: function(ev){
    var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth() + 1).padStart(2, '0');
      var yyyy = today.getFullYear();
      today = yyyy + '-' + mm + '-' + dd;
        $("#date_modal").attr("min",today)
        },
});

PublicWidget.registry.CreateReq = PublicWidget.Widget.extend({
    selector:'.s_website_form_rows.row.s_col_no_bgcolor',
    events: {
    'click #submit': '_CreateRequest',
    'change #machine': '_SetCustomer',
    'click #date': '_setDate',
    },
    _CreateRequest: function(ev){
    var year_val = new Date($('#date').val());
    var year = year_val.getFullYear();
    var month = year_val.getMonth();
    var date = year_val.getDate();
    if (year <= new Date().getFullYear() && month <= new Date().getMonth() && date < new Date().getDate())
    {
    alert("Cannot place a service request on past!")
    return false;
    }
    if (year > new Date().getFullYear() + 2){
    alert("Maximum up to above 2 years request can only be pre requested ")
    return false;
    }
    },

    _SetCustomer: function(ev){
    var self = this;
    ev.preventDefault();
    var machine = $("#machine").val()
    jsonrpc('/requestservice/customer', {
    "machine": machine,
    }).then(result=>{
    self.$el.find('#customer').empty()
    self.$el.find('#customer').append('<option>'+result.partner+'</option>')
    });
    },

    _setDate: function(ev){
    var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0');
  var yyyy = today.getFullYear();
  today = yyyy + '-' + mm + '-' + dd;
    $("#date").attr("min",today)
    },
   });
