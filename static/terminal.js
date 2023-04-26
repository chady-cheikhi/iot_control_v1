var hostnameDiv = document.getElementById('hostname');
var hostname = hostnameDiv.getAttribute('data-my-arg1');

$(document).on("submit","#terminal",function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/api/nano/'+hostname+'/terminal',
            data: {
                'custom_cmd': $('#custom_cmd').val(),
                'custom_cmd_output': ''
            },
            success: function (data)
            {
                console.log(data['status'])
            }
        })
    });
function terminal(){
        $.ajax({
            type: 'GET',
            url: '/api/nano/'+ hostname +'/terminal',
            success: function (response)
            {
                var output = $('#custom_cmd_output')
                output.empty()
                console.log(response)
                var temp= response['custom_cmd_output']
                console.log(temp)
                output.append(temp);
            },
            error: function(response){
                console.log('error');
            }
        })
    }

setInterval(terminal,2000);
