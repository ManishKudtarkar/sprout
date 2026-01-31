class RemedyRecommender:
    def get_remedies_for_condition(self, condition_data, user_profile=None):
        """
        Extracts and formats remedies for a given condition, filtering by user profile.
        """
        remedies = condition_data.get("remedies", [])
        if not remedies:
            return ["No specific natural remedies found for this condition."]
        
        if user_profile:
            remedies = self._personalize_remedies(remedies, user_profile)
            
        return remedies

    def _personalize_remedies(self, remedies, profile):
        body_type = profile.get("body_type", "neutral").lower()
        filtered_remedies = []
        
        # Simple rule-based exclusion
        for remedy in remedies:
            remedy_lower = remedy.lower()
            warning = None
            
            # Heat Body Rules (Avoid heating elements)
            if body_type == "heat":
                if any(x in remedy_lower for x in ["ginger", "pepper", "spicy", "hot", "garlic"]):
                    warning = " (Caution: May increase body heat)"
            
            # Cold Body Rules (Avoid cooling elements)
            if body_type == "cold":
                if any(x in remedy_lower for x in ["cold", "mint", "cucumber", "ice"]):
                    warning = " (Caution: May be too cooling)"

            if warning:
                filtered_remedies.append(remedy + warning)
            else:
                filtered_remedies.append(remedy)
                
        return filtered_remedies

    def explain_remedy(self, remedy_name):
        """
        Placeholder for future logic to explain why a remedy works.
        """
        # In a real system, this would query a knowledge base of mechanism of action.
        explanations = {
            "Ginger tea": "Ginger has anti-inflammatory properties and helps soothe the throat.",
            "Honey and lemon": "Honey coats the throat and lemon provides Vitamin C.",
            "Steam inhalation": "Helps clear nasal congestion.",
            "Rest": "Allows the body to focus energy on fighting the infection.",
            "Hydration": "Essential for bodily functions and recovery."
        }
        return explanations.get(remedy_name, "Natural aid for symptom relief.")
