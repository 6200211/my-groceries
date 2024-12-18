import { useContext, useState, useEffect } from "react";
import { Context } from "../../App";
import "./AccountPage.css";
import Checkbox from "../UI/Checkbox/Checkbox";
import { AuthApi } from "../../api/AuthApi";
import ErrorPopup from "../Modals/ErrorPopup/ErrorPopup";

export default function AccountPage() {
    const { user } = useContext(Context);

    useEffect(() => {
        console.log("User in AccountPage:", user);
    }, [user]);

    const [verificationCode, setVerificationCode] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [errorPopupIsOpen, setErrorPopupIsOpen] = useState(false);
    const [errorPopupMessage, setErrorPopupMessage] = useState('');
    
    const handleVerificationSubmit = async (event) => {
        event.preventDefault();
        const result = await AuthApi.verifyCode(user.email, verificationCode)
    
        if (!result.success) {
            setErrorPopupIsOpen(true);
            setErrorPopupMessage(result.message)
        } else {
            alert(result.message)
        }
    };

    const handleResendCode = async (event) => {
        event.preventDefault()
        try {
            const result = await AuthApi.sendVerificationCode(user.email);
            if (!result.success) {
                setErrorPopupIsOpen(true);
                setErrorPopupMessage(result.message);
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error("Verification error:", error.message);
            setErrorPopupIsOpen(true);
            setErrorPopupMessage("Something went wrong. Please try again later.");
        }
    }

    return (
        <>
            <div className="account-page">
                <h1>Account</h1>
                {user && user.isVerified === false && (
                <div className="verification-section">
                    <h2>Account Not Verified</h2>
                    <p>Your account is not verified yet. Please enter the verification code sent to your email.</p>
                    <form onSubmit={handleVerificationSubmit}>
                        <div className="form-group">
                            <label htmlFor="verification-code">Verification Code</label>
                            <input
                                className="text-input"
                                type="number"
                                id="verification-code"
                                value={verificationCode}
                                maxLength={6}
                                onChange={(e) => setVerificationCode(e.target.value)}
                                placeholder="Enter verification code"
                            />
                        </div>
                        {errorMessage && <p className="error-message">{errorMessage}</p>}
                        <div className="account--btn-container">
                            <button type="submit" className="btn" onClick={handleResendCode}>Resend code</button>
                            <button type="submit" className="btn" disabled={!verificationCode.trim()} onClick={handleVerificationSubmit}>Verify Account</button>
                        </div>
                    </form>
                </div>
                )}
                {user ? (
                    <form className="account-form">
                        <div>
                            {/* Full Name */}
                            <div className="form-section">
                                <h2>Full name</h2>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="first-name">First name</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="first-name"
                                            value={user.name || ""}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="last-name">Last name</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="last-name"
                                            value={user.surname || ""}
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Contact Email */}
                            <div className="form-section">
                                <h2>Contact e-mail</h2>
                                <div className="form-group">
                                    <label htmlFor="email">E-mail</label>
                                    <input
                                        className="text-input"
                                        type="email"
                                        id="email"
                                        value={user.email || ""}
                                        readOnly
                                    />
                                </div>
                            </div>

                            <div className="form-section">
                                <h2>Modify password</h2>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="current-password">Current password</label>
                                        <input
                                            className="text-input"
                                            type="password"
                                            id="current-password"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="new-password">New password</label>
                                        <input
                                            className="text-input"
                                            type="password"
                                            id="new-password"
                                        />
                                    </div>
                                </div>
                                <Checkbox label="Show password" />
                            </div>
                        </div>

                        <div>
                            {/* Address */}
                            <div className="form-section">
                                <h2>Address</h2>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="region">Region</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="region"
                                            value={user.region || ""}
                                            placeholder="Region name"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="city">City/town name</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="city"
                                            value={user.deliveryPlace || ""}
                                            placeholder="Nowhereville"
                                        />
                                    </div>
                                </div>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="street-address">Street address</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="street-address"
                                            value={user.street || ""}
                                            placeholder="Main street, 73, apt. 14"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="postal-code">Postal code</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="postal-code"
                                            value={user.postalCode || ""}
                                            placeholder="00000"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div className="form-section">
                                <h2>Payment details</h2>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="card-number">Card number</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="card-number"
                                            value={user.cardNumber || ""}
                                            placeholder="1111 1111 1111 1111"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="expiration-date">Expiration date</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="expiration-date"
                                            value={user.cardDate || ""}
                                            placeholder="01/30"
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="cvv">CVV</label>
                                        <input
                                            className="text-input"
                                            type="text"
                                            id="cvv"
                                            value={user.cardCVV || ""}
                                            placeholder="***"
                                        />
                                    </div>
                                </div>
                            </div>

                            <button type="button" className="btn">
                                Save details
                            </button>
                        </div>
                    </form>
                ) : (
                    <p>User data not available</p>
                )}
            </div>
            <ErrorPopup
                isOpen={errorPopupIsOpen}
                onClose={() => setErrorPopupIsOpen(false)}
                error={errorPopupMessage}
            />
        </>
    );
}
