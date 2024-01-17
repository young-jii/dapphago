(function() {
    var Message, url;
    Message = function(arg) {
        (this.text = arg.text), (this.message_side = arg.message_side);
        this.draw = (function(_this) {
            return function() {
                var $message;
                $message = $(
                    $('.message_template')
                        .clone()
                        .html()
                );
                $message
                    .addClass(_this.message_side)
                    .find('.text')
                    .html(_this.text);
                if (this.message_side === 'left') {
                    url = 'images/dapphago.png';
                } else {
                    url = 'images/user.png';
                }
                $message
                    .find('.avatar')
                    .css('background-image', 'url(../static/' + url + ')');
                $('.messages').append($message);
                return setTimeout(function() {
                    return $message.addClass('appeared');
                }, 0);
            };
        })(this);
        return this;
    };
    $(function() {
        var getMessageText, sendMessage;
        getMessageText = function() {
            var $message_input;
            $message_input = $('.message_input');
            return $message_input.val();
        };
        sendMessage = function(text) {
            var $messages, message, response;
            if (text.trim() === '') {
                return;
            }
            $('.message_input').val('');
            $messages = $('.messages');
            message = new Message({
                text: text,
                message_side: 'right'
            });
            message.draw();

            $.ajax({
                async: false,
                url: '/get_botresponse',
                dataType: 'text',
                type: 'POST',
                data: {
                    question: text,
                },
                success: function(data) {
                    console.log(data)
                    var response = JSON.parse(data);
                    var responseMessage = new Message({
                        text: response.response,
                        message_side: 'left'
                    });
                    responseMessage.draw();
                    // alert('success');
                },
                error:function(){
                    alert('fail');
                }
            });
            console.log("test");

            return $messages.stop().animate(
                { scrollTop: $messages.prop('scrollHeight') },
                700
            );
        };
        $('.send_message').click(function() {
            return sendMessage(getMessageText());
        });

        var message_greetings = new Message({
            text: '안녕하세요. 답파고입니다. 무엇을 도와드릴까요?',
            message_side: 'left'
        });
        message_greetings.draw();
    });
}.call(this));
