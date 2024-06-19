$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })

  <!-- Script JavaScript para capturar eventos de clique -->
<script>
    $(document).ready(function() {
        // Captura o clique no botão "Modificar"
        $('.btn-modificar').click(function() {
            var produtoId = $(this).data('produto-id');
            // Exemplo de abertura de modal (ou outra ação que você queira)
            console.log('Modificar produto com ID:', produtoId);
            // Aqui você pode abrir um modal, carregar dados via AJAX, etc.
            // Exemplo: abrir um modal de edição
            $('#exampleModal2Center').modal('show');
        });

        // Captura o clique no botão "Excluir"
        $('.btn-excluir').click(function() {
            var produtoId = $(this).data('produto-id');
            // Implemente a lógica para exclusão usando AJAX
            console.log('Excluir produto com ID:', produtoId);
            // Aqui você pode enviar uma requisição AJAX para excluir o produto
            // Exemplo:
            $.ajax({
                type: 'POST',
                url: '{% url 'excluir_produto' %}',
                data: {
                    'produto_id': produtoId,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function(response) {
                    // Exemplo de atualização da tabela após exclusão
                    // Atualizar a tabela ou remover a linha do produto excluído
                    // Exemplo: remover a linha da tabela
                    $('#linha-produto-' + produtoId).remove();
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText); // Log de erros, se necessário
                }
            });
        });
    });
</script>