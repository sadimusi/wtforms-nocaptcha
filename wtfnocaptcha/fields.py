from wtforms.fields import Field
# from wtforms.validators import Required

from . import widgets
from . import validators as local_validators

try:
    import flask
except ImportError:
    flask = None


class NoCaptchaField(Field):
    """Handles captcha field display and validation via No Captcha reCaptcha"""

    widget = widgets.NoCaptcha()

    def __init__(
            self, label='',
            validators=None,
            public_key=None,
            private_key=None,
            secure=False,
            http_proxy=None,
            **kwargs):
        # Pretty useless without the Recaptcha validator but still
        # user may want to subclass it, so keep it optional
        validators = validators or [local_validators.NoCaptcha()]
        super(NoCaptchaField, self).__init__(label, validators, **kwargs)

        if not flask and (not public_key or not private_key):
            raise ValueError(
                'Both recaptcha public and private keys are required.')
        self._public_key = public_key
        self._private_key = private_key
        self.secure = secure
        self.http_proxy = http_proxy

        self.ip_address = None

    @property
    def private_key(self):
        key = self._private_key
        if key is None:
            try:
                key = flask.current_app.config.get("RECAPTCHA_PRIVATE_KEY")
            except RuntimeError:
                pass
        if key is None:
            raise ValueError("No ReCAPTCHA private key is configured. "
                             "(RECAPTCHA_PRIVATE_KEY)")
        return key

    @property
    def public_key(self):
        key = self._public_key
        if key is None:
            try:
                key = flask.current_app.config.get("RECAPTCHA_PUBLIC_KEY")
            except RuntimeError:
                pass
        if key is None:
            raise ValueError("No ReCAPTCHA public key is configured. "
                             "(RECAPTCHA_PUBLIC_KEY)")
        return key

    def process(self, formdata, data={}):
        """Handles multiple formdata fields that are required for reCaptcha.
        Only response field is handled as raw_data as it is the only user input
        """
        self.process_errors = []
        ip_address = None

        if isinstance(data, dict):
            ip_address = data.pop('ip_address', None)

        try:
            self.process_data(data)
        except ValueError as e:
            self.process_errors.append(e.args[0])

        if formdata is not None:
            # Developer must supply ip_address directly so throw a
            # non-validation exception if it's not present
            if not ip_address and flask:
                try:
                    if "CF-Connecting-IP" in flask.request.headers:
                        ip_address = flask.request.headers["CF-Connecting-IP"]
                    else:
                        ip_address = flask.request.remote_addr
                except RuntimeError:
                    pass  # An exception will be raised below

            if not ip_address:
                    raise ValueError('IP address is required.')

            try:

                # Pass user input as the raw_data
                self.raw_data = formdata.getlist('g-recaptcha-response')
                self.process_formdata(self.raw_data)
            except ValueError as e:
                self.process_errors.append(e.args[0])

        for filter in self.filters:
            try:
                self.data = filter(self.data)
            except ValueError as e:
                self.process_errors.append(e.args[0])
