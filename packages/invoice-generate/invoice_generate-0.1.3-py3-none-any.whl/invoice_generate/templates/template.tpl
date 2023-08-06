<html>
    <head> 
        <meta charset="UTF-8">
        <style> 
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
            }
            body {
                width: 21cm;
                height: 29.7cm;
                margin: 5mm 10mm 5mm 10mm; 
            } 
            
        </style>
    </head>
  <body>
    <center>
        <big><b>Invoice/Інвойс</b> № {{invoice_number}}</big>
        <p/>
        
        <table style="width:100%">
            <tr> 
                <td> <b>Date of invoice:</b> {{ invoice_date }} </td>  <td> <b>Дата інвойсу:</b> {{ invoice_date }} </td>
            </tr>
            <tr>
                <td>
                    <b>Supplier:</b> {{ FULL_NAME_EN }} <br/>
                    <b>Address:</b> {{ ADDRESS_EN }} <br/>
                    <b>Individual tax number:</b> {{ TAX_NUMBER }}
                </td> 
                <td>
                    <b>Виконавець:</b> {{FULL_NAME_UK}}<br/>
                    <b>Адреса:</b> {{ ADDRESS_UK }} <br/>
                    <b>ІПН:</b> {{ TAX_NUMBER }}
                </td>
            </tr>
            
            <tr>
                <td>
                    <b>Customer:</b> {{ CUSTOMER_EN }} <br/>
                    <b>Address:</b> {{ CUSTOMER_ADDRESS_EN }}
                </td> 
                <td>
                    <b>Замовник:</b> {{ CUSTOMER_EN }}<br/>
                    <b>Адреса:</b> {{ CUSTOMER_ADDRESS_EN }}
                </td>
            </tr>
            
            <tr>
                <td>
                    <b>Description:</b> Consulting on informatization
                </td>   
                <td>
                    <b>Опис:</b> Консультування з питань інформатизації
                </td>
            </tr>
            
            <tr>
                <td><b>Currency:</b> USD</td> <td><b>Валюта:</b> долар США</td>
            </tr>
            <tr>    
                <td colspan="2">
                    <p>
                        <b>Supplier bank information: </b><br/>
                        <b>Beneficiary:</b> PE {{ FULL_NAME_EN }} <br/>
                        <b>IBAN Code:</b> {{ SUPPLIER_IBAN }} <br/>
                        <b>Beneficiary’s bank:</b> {{ SUPPLIER_BANK }} <br/>
                        <b>SWIFT code:</b> {{ SUPPLIER_SWIFT }} <br/>
                    </p>

                    <p>
                        <b>Correspondent bank:</b> <br/>
                        <b>Bank name:</b> {{ CORRESPONDENT_BANK }} <br/>
                        <b>SWIFT code:</b> {{ CORRESPONDENT_SWIFT }} <br/>
                    </p>
                </td>
            </tr>
        </table>
        
        <p></p>
        
        <table style="width:100%">
            <tr>
                <th><b>№</b></th> <th style="text-align:left"><b>Description / Опис</b></th> <th><b>Amount, USD / Сума, долар США</b></th>
            </tr>
            
            <tr>
                <td>1</td>
                <td>
                    Services in accordance with the Contract # {{ CONTRACT_NUMBER }} dated {{ CONTRACT_DATE_EN }}, work period from {{ start_date_en }} till {{ end_date_en }} /
                    Послуги на підставі Договору № {{ CONTRACT_NUMBER }}  від {{ CONTRACT_DATE_UK }}, термін робіт з {{ start_date_uk }} до {{ end_date_uk }}.
                </td>
                <td>{{ '{0:0.2f}'.format(AMOUNT) }}</td>
            </tr>
                        
            <tr>
            <td>2</td> <td>Commission compensation / Компенсація комісії</td> <td>{{ '{0:0.2f}'.format(COMMISSION_AMOUNT) }}</td>
            </tr>
                        
            <tr>
            <td>3</td> <td>Total to pay / Всього до сплати:</td> <td>{{ '{0:0.2f}'.format(total) }}</td>
            </tr>
        </table>
    </center> 
    <p>Pay within 5 days/Сплатити протягом 5 днів</p>

    <p><small>Please note, that payment according to this invoice at the same time is the confirmation of performed works, delivered services and final mutual installments between Parties without any additional documents. Also it is to acknowledge that Parties have no claims to each other. / Оплата згідно цього Інвойсу одночасно є підтвердженням виконаних робіт, наданих послуг, кінцевих розрахунків між Сторонами і того, що Сторони не мають взаємних претензій, і не вимагає підписання додаткових документів</small></p>
    
    <p>Supplier/Виконавець: <img src="{{ SUPPLIER_SIGNATURE_URL }}" style="width:215px;height:159px;"> </img> ({{ FIRST_AND_LAST_NAME_EN }} / {{ FIRST_AND_LAST_NAME_UK }}) </p>
   
  </body>
</html>
