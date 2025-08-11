pip install awscli
cat ~/.aws/config 
export AWS_BEARER_TOKEN_BEDROCK=ABSKYXRoZW5hemhhbmdAam9obnNvbmZpdG5lc3MuY29tLWF0LTM1OTU2NDk3NzE5MzpRUHh0NWZxT2R0dkpSV2lYcWxqbEw3eWQvRVFUU0x2ak8zRVRoTkZpK2VUN2lTaENmWENSTlVKMjBwQT0=
aws bedrock list-foundation-models --profile jht-ai --region ap-northeast-1
env | grep ^AWS_     
aws configure --profile jht-ai
aws configure list --profile default
aws configure list-profiles 
