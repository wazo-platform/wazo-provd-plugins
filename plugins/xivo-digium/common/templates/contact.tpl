<phonebooks>
    <contacts group_name="Default" editable="0">
        {% for funckey_no, funckey in XX_funckeys.iteritems()|sort %}
        <contact
        first_name="{{ funckey['label']|d(funckey['value']) }}"
        last_name=""
        {% if funckey['type'] == 'blf' %}
        subscribe_to="sip:{{ funckey['value'] }}@{{ XX_main_proxy_ip }}"
        {% endif %}
        >
            <numbers>
                <number dial="{{ funckey['value'] }}" label="Extension" primary="1" />
            </numbers>
        </contact>
        {% endfor %}
     </contacts>
</phonebooks>
