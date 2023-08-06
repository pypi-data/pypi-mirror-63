#include "FirebaseRemoteConfig.h"
#include "firebase/remote_config.h"

using namespace firebase;

const char* ValueSourceToString(firebase::remote_config::ValueSource source) {
	static const char* kSourceToString[] = {
	  "Static",   // kValueSourceStaticValue
	  "Remote",   // kValueSourceRemoteValue
	  "Default",  // kValueSourceDefaultValue
	};
	return kSourceToString[source];
}


FirebaseRemoteConfig::FirebaseRemoteConfig()
{
	LOG("FirebaseRemoteConfig()");
}
FirebaseRemoteConfig::~FirebaseRemoteConfig()
{
	LOG("~FirebaseRemoteConfig()");
}

void FirebaseRemoteConfig::init()
{	
}

void FirebaseRemoteConfig::release()
{	
}

std::string FirebaseRemoteConfig::getString(const char* key)
{
	remote_config::ValueInfo value_info;
	auto result = remote_config::GetString(key, &value_info);

	LOG("Get key=%s <%s>=<%s>", key, result.c_str(), ValueSourceToString(value_info.source));

	return result;
}

long FirebaseRemoteConfig::GetLong(const char* key)
{
	remote_config::ValueInfo value_info;
	auto result = remote_config::GetLong(key, &value_info);

	LOG("Get key=%s <%ld>=<%s>", key, result, ValueSourceToString(value_info.source));

	return result;
}

double FirebaseRemoteConfig::GetDouble(const char* key)
{
	remote_config::ValueInfo value_info;
	auto result = remote_config::GetDouble(key, &value_info);

	LOG("Get key=%s <%lf>=<%s>", key, result, ValueSourceToString(value_info.source));

	return result;
}

bool FirebaseRemoteConfig::GetBoolean(const char* key)
{
	remote_config::ValueInfo value_info;
	auto result = remote_config::GetBoolean(key, &value_info);

	LOG("Get key=%s <%d>=<%s>", key, result, ValueSourceToString(value_info.source));

	return result;
}