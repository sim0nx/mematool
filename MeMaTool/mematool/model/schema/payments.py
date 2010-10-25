import formencode

class PaymentForm(formencode.Schema):
        allow_extra_fields = True
        filter_extra_fields = True
        idpayment = formencode.validators.Int()
        dtreason = formencode.validators.String()
        dtdate = formencode.validators.String(not_empty=True)
	# below does not work with the current format
	#dtdate = formencode.validators.DateConverter(not_empty=True)	
        dtamount = formencode.validators.Int(not_empty=True)
        limember = formencode.validators.Int(not_empty=True)
        lipaymentmethod = formencode.validators.Int(not_empty=True)
