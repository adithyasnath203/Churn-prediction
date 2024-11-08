import json
import pandas as pd
from django.shortcuts import render
from django.views.generic import TemplateView
from ml.ml_model import predict, make_data_uniform,  change_totalcharge_to_int
from Email.tasks import send_email_task


class Home(TemplateView):
    template_name = "functions/home.html"


class ChurnFinderView(TemplateView):
    template_name = "functions/churn_finder.html"

    def post(self, request, *args, **kwargs):
        customer = {**request.POST.dict()}
        numerical_field = ["tenure", "monthlycharges", "totalcharges", "seniorcitizen"]
        for field in numerical_field:
            customer[field] = float(customer[field])
        customer.pop("csrfmiddlewaretoken", None)
        email = customer.pop("email", None)
        prediction = predict(customer)
        is_churn = 1 if prediction[0][1] >= 0.5 else 0
        return render(
            request, self.template_name, {"is_churn": is_churn, "predicted": True, 'email': email}
        )


class SendEmailView(TemplateView):
    template_name = "functions/send_email.html"

    def post(self, request, *args, **kwargs):
        email_id = self.request.POST.get('email')
        send_email_task(email_id)
        return render(request, self.template_name, {"sent": True})


class BulkEmailView(TemplateView):
    template_name = "functions/bulk_email.html"
    def post(self, request, *args, **kwargs):
        churning_customers = [json.loads(customer) for customer in request.session['churning_customers']]
        for customer in churning_customers:
            send_email_task(customer['email'])
        return render(request, self.template_name, {})


class BulkChurnFinder(TemplateView):
    template_name = "functions/bulk_find.html"

    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        df = pd.read_csv(file)
        df = make_data_uniform(df)
        df = change_totalcharge_to_int(df)
        churning_customers = []
        non_churning_customers = []
        for index, row in df.iterrows():
            email = row.pop('email')
            customer = row
            prediction = predict(customer)
            customer['email'] = email
            if prediction[0][1] >= 0.5:
                churning_customers.append(customer)
            else:
                non_churning_customers.append(customer)
        request.session['churning_customers'] = [customer.to_json() for customer in churning_customers]
        return render(request, self.template_name, {'churning_customers': churning_customers, 'non_churning_customers': non_churning_customers})