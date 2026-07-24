{% macro player_image_url(player_code_column) %}
    case
        when {{ player_code_column }} is null then null
        else
            'https://resources.premierleague.com/premierleague/photos/players/110x140/p'
            || {{ player_code_column }}::text
            || '.png'
    end
{% endmacro %}
